"""Authentication session model with durable browser-session cookie state."""

from __future__ import annotations

import datetime as dt
from typing import Any, Optional

from tigrbl_identity_storage.framework import (
    Base,
    BaseModel,
    Depends,
    HTTPException,
    Request,
    TenantColumn,
    Timestamped,
    TigrblRouter,
    UserColumn,
    S,
    acol,
    Mapped,
    String,
    TZDateTime,
    GUIDPk,
    ForeignKeySpec,
    PgUUID,
    UUID,
    Field,
    constr,
    status,
)
from ..user import MyAccountMutationOut, User, _current_principal_dependency, _iso, _not_found_uuid
from .._ops import create_record, field, first_record, list_records, read_record, record_id, update_record, utc_now
from ..engine import get_db

_password = constr(min_length=8, max_length=256)


class CredsIn(BaseModel):
    identifier: constr(strip_whitespace=True, min_length=3, max_length=120)
    password: _password


class TokenPair(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = Field(default="bearer")
    id_token: Optional[str] = None


class MyAccountSessionOut(BaseModel):
    id: str
    tenant_id: str
    user_id: str
    username: str
    client_id: str | None = None
    state: str = "active"
    auth_time: str | None = None
    last_seen_at: str | None = None
    expires_at: str | None = None
    ended_at: str | None = None


class AuthSession(Base, GUIDPk, Timestamped, UserColumn, TenantColumn):
    __tablename__ = "sessions"
    __table_args__ = ({"schema": "authn"},)

    username: Mapped[str] = acol(storage=S(String(120), nullable=False))
    client_id: Mapped[UUID | None] = acol(
        storage=S(PgUUID(as_uuid=True), fk=ForeignKeySpec(target="authn.clients.id"), nullable=True, index=True)
    )
    auth_time: Mapped[dt.datetime] = acol(
        storage=S(TZDateTime, nullable=False, default=lambda: dt.datetime.now(dt.timezone.utc))
    )
    session_state: Mapped[str] = acol(storage=S(String(64), nullable=False, default="active"))
    session_state_salt: Mapped[str | None] = acol(storage=S(String(128), nullable=True))
    cookie_secret_hash: Mapped[str | None] = acol(storage=S(String(128), nullable=True, index=True))
    cookie_issued_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True))
    cookie_rotated_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True))
    expires_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))
    last_seen_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True))
    ended_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))
    logout_reason: Mapped[str | None] = acol(storage=S(String(128), nullable=True))

    @classmethod
    async def create_for_user(
        cls,
        db: Any,
        *,
        user_id: UUID,
        tenant_id: UUID,
        username: str,
        client_id: UUID | None = None,
        expires_at: dt.datetime | None = None,
        cookie_secret_hash: str | None = None,
        session_state_salt: str | None = None,
        **extra: Any,
    ) -> "AuthSession":
        now = utc_now()
        payload = {
            "user_id": user_id,
            "tenant_id": tenant_id,
            "username": username,
            "client_id": client_id,
            "auth_time": now,
            "session_state": "active",
            "session_state_salt": session_state_salt,
            "cookie_secret_hash": cookie_secret_hash,
            "cookie_issued_at": now if cookie_secret_hash else None,
            "cookie_rotated_at": now if cookie_secret_hash else None,
            "expires_at": expires_at,
            "last_seen_at": now,
        }
        payload.update(extra)
        return await create_record(cls, db, payload)

    @classmethod
    async def list_for_user(
        cls,
        db: Any,
        *,
        user_id: UUID,
        tenant_id: UUID | None = None,
        active_only: bool = True,
    ) -> list["AuthSession"]:
        filters: dict[str, Any] = {"user_id": user_id}
        if tenant_id is not None:
            filters["tenant_id"] = tenant_id
        rows = await list_records(cls, db, filters)
        if not active_only:
            return rows
        now = utc_now()
        return [
            row
            for row in rows
            if field(row, "ended_at") is None
            and str(field(row, "session_state", "active")).lower() not in {"terminated", "ended", "revoked", "expired"}
            and (field(row, "expires_at") is None or field(row, "expires_at") > now)
        ]

    @classmethod
    async def revoke_for_user(
        cls,
        db: Any,
        *,
        session_id: UUID,
        user_id: UUID | None = None,
        reason: str = "revoked",
    ) -> "AuthSession | None":
        row = await read_record(cls, db, session_id)
        if row is None or (user_id is not None and str(field(row, "user_id")) != str(user_id)):
            return None
        return await update_record(
            cls,
            db,
            record_id(row) or session_id,
            {"session_state": "revoked", "ended_at": utc_now(), "logout_reason": reason},
        )

    @classmethod
    async def revoke_all_for_user(
        cls,
        db: Any,
        *,
        user_id: UUID,
        tenant_id: UUID | None = None,
        reason: str = "revoked",
    ) -> list["AuthSession"]:
        revoked = []
        for row in await cls.list_for_user(db, user_id=user_id, tenant_id=tenant_id):
            updated = await cls.revoke_for_user(db, session_id=record_id(row), user_id=user_id, reason=reason)
            if updated is not None:
                revoked.append(updated)
        return revoked

    @classmethod
    async def touch(cls, db: Any, *, session_id: UUID) -> "AuthSession | None":
        row = await first_record(cls, db, {"id": session_id})
        if row is None:
            row = await read_record(cls, db, session_id)
        if row is None:
            return None
        return await update_record(cls, db, record_id(row) or session_id, {"last_seen_at": utc_now()})


account_api = account_router = TigrblRouter()
login_api = login_router = TigrblRouter()
MY_ACCOUNT_TAGS = ["My Account"]


def _session_payload(session: AuthSession) -> MyAccountSessionOut:
    return MyAccountSessionOut(
        id=str(session.id),
        tenant_id=str(session.tenant_id),
        user_id=str(session.user_id),
        username=str(session.username),
        client_id=str(session.client_id) if session.client_id is not None else None,
        state=str(session.session_state or "active"),
        auth_time=_iso(getattr(session, "auth_time", None)),
        last_seen_at=_iso(getattr(session, "last_seen_at", None)),
        expires_at=_iso(getattr(session, "expires_at", None)),
        ended_at=_iso(getattr(session, "ended_at", None)),
    )


@account_api.route(
    "/account/sessions",
    methods=["GET"],
    response_model=list[MyAccountSessionOut],
    tags=MY_ACCOUNT_TAGS,
)
async def list_account_sessions(
    current_user: User = Depends(_current_principal_dependency),
    db: Any = Depends(get_db),
) -> list[MyAccountSessionOut]:
    rows = await list_records(
        AuthSession,
        db,
        {"user_id": current_user.id, "tenant_id": current_user.tenant_id},
    )
    return [_session_payload(row) for row in rows]


@account_api.route(
    "/account/sessions/{session_id}",
    methods=["DELETE"],
    response_model=MyAccountMutationOut,
    tags=MY_ACCOUNT_TAGS,
)
async def revoke_account_session(
    session_id: str,
    current_user: User = Depends(_current_principal_dependency),
    db: Any = Depends(get_db),
) -> MyAccountMutationOut:
    session_uuid = _not_found_uuid(session_id, field="session")
    row = await read_record(AuthSession, db, session_uuid)
    if row is not None and (
        str(getattr(row, "user_id", "")) != str(current_user.id)
        or str(getattr(row, "tenant_id", "")) != str(current_user.tenant_id)
    ):
        row = None
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "session not found")
    updated = await update_record(
        AuthSession,
        db,
        row.id,
        {
            "session_state": "revoked",
            "ended_at": row.ended_at or utc_now(),
            "logout_reason": row.logout_reason or "account_self_service",
        },
    )
    return MyAccountMutationOut(status="revoked", id=str(updated.id))


AuthSession.list_account_sessions = staticmethod(list_account_sessions)  # type: ignore[attr-defined]
AuthSession.revoke_account_session = staticmethod(revoke_account_session)  # type: ignore[attr-defined]


@login_api.route("/login", methods=["POST"], response_model=TokenPair)
async def login(
    request: Request,
    creds: CredsIn | None = None,
    db: Any = Depends(get_db),
) -> Any:
    from ._op import login_user

    if creds is None:
        body = await request.json() or {}
        creds = CredsIn.model_validate(body)
    return await login_user(
        request=request,
        db=db,
        identifier=creds.identifier,
        password=creds.password,
    )


AuthSession.login = staticmethod(login)  # type: ignore[attr-defined]


__all__ = [
    "AuthSession",
    "CredsIn",
    "MyAccountSessionOut",
    "TokenPair",
    "account_api",
    "account_router",
    "login_api",
    "login_router",
    "list_account_sessions",
    "login",
    "revoke_account_session",
]
