"""AuthSession-owned lifecycle helpers formerly exposed by storage persistence."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from .._ops import field, read_handler_record, update_handler_record
from .._session import storage_session
from .._sync import run_async
from ._table import AuthSession


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
        return await AuthSession.create_for_user(
            db,
            user_id=user_id,
            tenant_id=tenant_id,
            username=username,
            client_id=client_id,
            expires_at=expires_at,
            cookie_secret_hash=cookie_secret_hash,
            session_state_salt=session_state_salt,
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


create_session = lambda **kwargs: run_async(create_session_async(**kwargs))
touch_session = lambda session_id: run_async(touch_session_async(session_id))
get_session = lambda session_id: run_async(get_session_async(session_id))
get_active_session = lambda session_id: run_async(get_active_session_async(session_id))
rotate_session_cookie_secret = lambda session_id, **kwargs: run_async(
    rotate_session_cookie_secret_async(session_id, **kwargs)
)
bind_session_client = lambda session_id, **kwargs: run_async(bind_session_client_async(session_id, **kwargs))


__all__ = [
    "bind_session_client",
    "bind_session_client_async",
    "create_session",
    "create_session_async",
    "get_active_session",
    "get_active_session_async",
    "get_session",
    "get_session_async",
    "rotate_session_cookie_secret",
    "rotate_session_cookie_secret_async",
    "touch_session",
    "touch_session_async",
]
