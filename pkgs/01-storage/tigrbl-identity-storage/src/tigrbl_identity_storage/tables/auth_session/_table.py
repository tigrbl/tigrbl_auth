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
    op_ctx,
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


def _created(result: Any) -> Any:
    if isinstance(result, dict):
        for key in ("item", "result", "data"):
            if key in result:
                return result[key]
    return result


def _field(row: Any, key: str, default: Any = None) -> Any:
    if row is None:
        return default
    if isinstance(row, dict):
        return row.get(key, default)
    return getattr(row, key, default)


@op_ctx(
    bind=AuthSession,
    alias="terminate",
    target="custom",
    arity="member",
    rest=False,
)
async def terminate(cls: type[AuthSession], ctx: dict[str, Any]) -> AuthSession | None:
    payload = dict(ctx.get("payload") or {})
    session_id = payload.get("session_id") or payload.get("id") or dict(ctx.get("path_params") or {}).get("id")
    row = await cls.handlers.read.core({"path_params": {"id": session_id}, "db": ctx["db"]})
    if row is None:
        return None
    now = utc_now()
    return _created(
        await cls.handlers.update.core(
            {
                "path_params": {"id": session_id},
                "payload": {
                    "session_state": payload.get("session_state") or "terminated",
                    "ended_at": _field(row, "ended_at") or now,
                    "logout_reason": payload.get("reason") or _field(row, "logout_reason") or "logout",
                },
                "db": ctx["db"],
            }
        )
    )


@op_ctx(
    bind=AuthSession,
    alias="touch",
    target="custom",
    arity="member",
    rest=False,
)
async def touch(cls: type[AuthSession], ctx: dict[str, Any]) -> AuthSession | None:
    payload = dict(ctx.get("payload") or {})
    session_id = payload.get("session_id") or payload.get("id") or dict(ctx.get("path_params") or {}).get("id")
    row = await cls.handlers.read.core({"path_params": {"id": session_id}, "db": ctx["db"]})
    if row is None:
        return None
    return _created(
        await cls.handlers.update.core(
            {
                "path_params": {"id": session_id},
                "payload": {"last_seen_at": utc_now()},
                "db": ctx["db"],
            }
        )
    )


@op_ctx(
    bind=AuthSession,
    alias="get_active",
    target="custom",
    arity="member",
    rest=False,
)
async def get_active(cls: type[AuthSession], ctx: dict[str, Any]) -> AuthSession | None:
    payload = dict(ctx.get("payload") or {})
    session_id = payload.get("session_id") or payload.get("id") or dict(ctx.get("path_params") or {}).get("id")
    row = await cls.handlers.read.core({"path_params": {"id": session_id}, "db": ctx["db"]})
    if row is None:
        return None
    if _field(row, "ended_at") is not None or str(_field(row, "session_state")).lower() in {
        "terminated",
        "ended",
        "revoked",
    }:
        return None
    expires_at = _field(row, "expires_at")
    if expires_at is not None:
        expiry = expires_at if expires_at.tzinfo is not None else expires_at.replace(tzinfo=dt.timezone.utc)
        if expiry <= dt.datetime.now(dt.timezone.utc):
            await cls.handlers.update.core(
                {
                    "path_params": {"id": session_id},
                    "payload": {
                        "session_state": "expired",
                        "ended_at": _field(row, "ended_at") or utc_now(),
                    },
                    "db": ctx["db"],
                }
            )
            return None
    return row


@op_ctx(
    bind=AuthSession,
    alias="rotate_cookie_secret",
    target="custom",
    arity="member",
    rest=False,
)
async def rotate_cookie_secret(cls: type[AuthSession], ctx: dict[str, Any]) -> AuthSession | None:
    payload = dict(ctx.get("payload") or {})
    session_id = payload.get("session_id") or payload.get("id") or dict(ctx.get("path_params") or {}).get("id")
    row = await cls.handlers.read.core({"path_params": {"id": session_id}, "db": ctx["db"]})
    if row is None:
        return None
    now = utc_now()
    return _created(
        await cls.handlers.update.core(
            {
                "path_params": {"id": session_id},
                "payload": {
                    "cookie_secret_hash": payload.get("cookie_secret_hash"),
                    "cookie_rotated_at": now,
                    "cookie_issued_at": _field(row, "cookie_issued_at") or now,
                    "last_seen_at": now,
                },
                "db": ctx["db"],
            }
        )
    )


@op_ctx(
    bind=AuthSession,
    alias="bind_client",
    target="custom",
    arity="member",
    rest=False,
)
async def bind_client(cls: type[AuthSession], ctx: dict[str, Any]) -> AuthSession | None:
    payload = dict(ctx.get("payload") or {})
    session_id = payload.get("session_id") or payload.get("id") or dict(ctx.get("path_params") or {}).get("id")
    row = await cls.handlers.read.core({"path_params": {"id": session_id}, "db": ctx["db"]})
    if row is None:
        return None
    return _created(
        await cls.handlers.update.core(
            {
                "path_params": {"id": session_id},
                "payload": {"client_id": payload.get("client_id"), "last_seen_at": utc_now()},
                "db": ctx["db"],
            }
        )
    )


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
