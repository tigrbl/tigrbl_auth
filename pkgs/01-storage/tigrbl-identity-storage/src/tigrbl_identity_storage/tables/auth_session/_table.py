"""Authentication session model with durable browser-session cookie state."""

from __future__ import annotations

import datetime as dt
from typing import Any, Optional

from tigrbl_identity_storage.framework import (
    RestOltpTable,
    BaseModel,
    Depends,
    HTTPException,
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
from .._ops import list_records, read_record, update_record, utc_now
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


class AuthSession(RestOltpTable, GUIDPk, Timestamped, UserColumn, TenantColumn):
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


account_api = account_router = TigrblRouter()
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


__all__ = [
    "AuthSession",
    "CredsIn",
    "MyAccountSessionOut",
    "TokenPair",
    "account_api",
    "account_router",
    "list_account_sessions",
    "revoke_account_session",
]
