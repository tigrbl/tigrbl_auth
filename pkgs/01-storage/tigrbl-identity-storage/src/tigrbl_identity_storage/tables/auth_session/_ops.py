from __future__ import annotations

import secrets
from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import UUID

from .._ops import create_record, field, read_handler_record, update_handler_record
from .._sync import run_async
from ..engine import storage_session
from ._table import AuthSession


async def login_user(*, request, db, identifier: str, password: str) -> Any:
    from tigrbl_auth_protocol_oidc.id_token import mint_id_token
    from tigrbl_auth_protocol_oauth.standards.authorization_server_metadata import ISSUER
    from tigrbl_identity_jose.jwt_coder import JWTCoder
    from tigrbl_identity_runtime.http_standards.cookies import issue_session_cookie, session_cookie_policy
    from tigrbl_identity_runtime.settings import settings
    from tigrbl_identity_server.rest.shared import _require_tls
    from tigrbl_identity_server.security.handler_records import (
        append_audit_event_record,
        create_browser_session_record,
        issue_token_pair_records,
    )
    from tigrbl_identity_server.security.user_lookup import first_user_by_filters
    from tigrbl_identity_storage.framework import HTTPException, JSONResponse

    _require_tls(request)
    row = await first_user_by_filters(db, {"username": identifier})
    if row is None:
        row = await first_user_by_filters(db, {"email": identifier})
    if row is None or not getattr(row, "is_active", True) or not row.verify_password(password):
        raise HTTPException(status_code=400, detail="invalid credentials")

    expires_at = datetime.now(timezone.utc) + timedelta(seconds=max(int(session_cookie_policy().max_age_seconds), 60))
    session_row, cookie_secret = await create_browser_session_record(
        db,
        user_id=row.id,
        tenant_id=row.tenant_id,
        username=row.username,
        expires_at=expires_at,
    )
    jwt = await JWTCoder.async_default()
    access, refresh = await issue_token_pair_records(
        db,
        jwt=jwt,
        sub=str(session_row.user_id),
        tid=str(session_row.tenant_id),
        client_id=None,
        scope="openid profile email",
        issuer=ISSUER,
        audience=settings.protected_resource_identifier,
    )
    id_token = await mint_id_token(
        sub=str(session_row.user_id),
        aud=ISSUER,
        nonce=secrets.token_urlsafe(8),
        issuer=ISSUER,
        sid=str(session_row.id),
        auth_time=int((session_row.auth_time or datetime.now(timezone.utc)).timestamp()),
    )
    response = JSONResponse(
        {
            "access_token": access,
            "refresh_token": refresh,
            "token_type": "bearer",
            "id_token": id_token,
            "session_id": str(session_row.id),
            "cookie_policy": {
                "name": session_cookie_policy().name,
                "same_site": session_cookie_policy().same_site,
                "secure": session_cookie_policy().secure,
            },
        }
    )
    issue_session_cookie(response, session_id=session_row.id, secret=cookie_secret, expires_at=session_row.expires_at)
    await append_audit_event_record(
        db,
        tenant_id=session_row.tenant_id,
        actor_user_id=session_row.user_id,
        session_id=session_row.id,
        event_type="session.login",
        target_type="session",
        target_id=str(session_row.id),
        details={"identifier": identifier},
    )
    commit = getattr(db, "commit", None)
    if callable(commit):
        result = commit()
        if hasattr(result, "__await__"):
            await result
    return response


async def create_session_async(
    *,
    user_id: UUID,
    tenant_id: UUID,
    username: str,
    client_id: UUID | None = None,
    expires_at: datetime | None = None,
    cookie_secret_hash: str | None = None,
    session_state_salt: str | None = None,
) -> AuthSession:
    async with storage_session() as db:
        return await create_record(
            AuthSession,
            db,
            {
                "user_id": user_id,
                "tenant_id": tenant_id,
                "username": username,
                "client_id": client_id,
                "expires_at": expires_at,
                "cookie_secret_hash": cookie_secret_hash,
                "session_state_salt": session_state_salt,
            },
        )


async def touch_session_async(session_id: UUID) -> AuthSession | None:
    async with storage_session() as db:
        return await AuthSession.touch(db, session_id=session_id)


async def get_session_async(session_id: UUID) -> AuthSession | None:
    async with storage_session() as db:
        return await read_handler_record(AuthSession, db, session_id)


async def get_active_session_async(session_id: UUID) -> AuthSession | None:
    async with storage_session() as db:
        row = await read_handler_record(AuthSession, db, session_id)
        if row is None:
            return None
        if field(row, "ended_at") is not None or str(field(row, "session_state")).lower() in {
            "terminated",
            "ended",
            "revoked",
        }:
            return None
        expires_at = field(row, "expires_at")
        if expires_at is not None:
            expiry = expires_at if expires_at.tzinfo is not None else expires_at.replace(tzinfo=timezone.utc)
            if expiry <= datetime.now(timezone.utc):
                await update_handler_record(
                    AuthSession,
                    db,
                    session_id,
                    {"session_state": "expired", "ended_at": field(row, "ended_at") or datetime.now(timezone.utc)},
                )
                return None
        return row


async def rotate_session_cookie_secret_async(session_id: UUID, *, cookie_secret_hash: str) -> AuthSession | None:
    async with storage_session() as db:
        row = await read_handler_record(AuthSession, db, session_id)
        if row is None:
            return None
        now = datetime.now(timezone.utc)
        return await update_handler_record(
            AuthSession,
            db,
            session_id,
            {
                "cookie_secret_hash": cookie_secret_hash,
                "cookie_rotated_at": now,
                "cookie_issued_at": field(row, "cookie_issued_at") or now,
                "last_seen_at": now,
            },
        )


async def bind_session_client_async(session_id: UUID, *, client_id: UUID | None) -> AuthSession | None:
    async with storage_session() as db:
        row = await read_handler_record(AuthSession, db, session_id)
        if row is None:
            return None
        return await update_handler_record(
            AuthSession,
            db,
            session_id,
            {"client_id": client_id, "last_seen_at": datetime.now(timezone.utc)},
        )


def create_session(**kwargs):
    return run_async(create_session_async(**kwargs))
def touch_session(session_id):
    return run_async(touch_session_async(session_id))
def get_session(session_id):
    return run_async(get_session_async(session_id))
def get_active_session(session_id):
    return run_async(get_active_session_async(session_id))
def rotate_session_cookie_secret(session_id, **kwargs):
    return run_async(
    rotate_session_cookie_secret_async(session_id, **kwargs)
)
def bind_session_client(session_id, **kwargs):
    return run_async(bind_session_client_async(session_id, **kwargs))


__all__ = [
    "bind_session_client",
    "bind_session_client_async",
    "create_session",
    "create_session_async",
    "get_active_session",
    "get_active_session_async",
    "get_session",
    "get_session_async",
    "login_user",
    "rotate_session_cookie_secret",
    "rotate_session_cookie_secret_async",
    "touch_session",
    "touch_session_async",
]
