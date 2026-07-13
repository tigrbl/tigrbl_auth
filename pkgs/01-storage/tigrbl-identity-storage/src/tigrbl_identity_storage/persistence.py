"""Deprecated compatibility facade for table-owned storage lifecycle helpers."""

from __future__ import annotations

import warnings
from datetime import datetime
from datetime import timezone
from typing import Any
from uuid import UUID

from tigrbl_identity_storage.tables._ops import delete_record, list_records, record_id, token_hash
from tigrbl_identity_storage.tables.audit_event import append_audit_event, append_audit_event_async
from tigrbl_identity_storage.tables._sync import run_async
from tigrbl_identity_storage.tables.auth_session import AuthSession
from tigrbl_identity_storage.tables.client_registration import ClientRegistration
from tigrbl_identity_storage.tables.consent import Consent
from tigrbl_identity_storage.tables.engine import storage_session
from tigrbl_identity_storage.tables.logout_state import LogoutState
from tigrbl_identity_storage.tables.revoked_token import RevokedToken
from tigrbl_identity_storage.tables.token_record import TokenRecord
from tigrbl_identity_runtime.settings import settings

warnings.warn(
    "tigrbl_identity_storage.persistence is deprecated; import lifecycle helpers from "
    "tigrbl_identity_storage.tables.<table> modules instead.",
    DeprecationWarning,
    stacklevel=2,
)


def _items(result):
    if isinstance(result, dict) and isinstance(result.get("items"), list):
        return result["items"]
    if isinstance(result, list):
        return result
    if isinstance(result, tuple):
        return list(result)
    return [] if result is None else [result]


def _created(result):
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
        return _created(
            await AuthSession.handlers.create.core(
                {
                    "payload": {
                        "user_id": user_id,
                        "tenant_id": tenant_id,
                        "username": username,
                        "client_id": client_id,
                        "expires_at": expires_at,
                        "cookie_secret_hash": cookie_secret_hash,
                        "session_state_salt": session_state_salt,
                    },
                    "db": db,
                }
            )
        )


async def touch_session_async(session_id: UUID) -> AuthSession | None:
    async with storage_session() as db:
        return await AuthSession.handlers.touch.core(
            {"path_params": {"id": session_id}, "payload": {"session_id": session_id}, "db": db}
        )


async def get_session_async(session_id: UUID) -> AuthSession | None:
    async with storage_session() as db:
        return await AuthSession.handlers.read.core({"path_params": {"id": session_id}, "db": db})


async def get_active_session_async(session_id: UUID) -> AuthSession | None:
    async with storage_session() as db:
        return await AuthSession.handlers.get_active.core(
            {"path_params": {"id": session_id}, "payload": {"session_id": session_id}, "db": db}
        )


async def rotate_session_cookie_secret_async(session_id: UUID, *, cookie_secret_hash: str) -> AuthSession | None:
    async with storage_session() as db:
        return await AuthSession.handlers.rotate_cookie_secret.core(
            {
                "path_params": {"id": session_id},
                "payload": {"session_id": session_id, "cookie_secret_hash": cookie_secret_hash},
                "db": db,
            }
        )


async def bind_session_client_async(session_id: UUID, *, client_id: UUID | None) -> AuthSession | None:
    async with storage_session() as db:
        return await AuthSession.handlers.bind_client.core(
            {
                "path_params": {"id": session_id},
                "payload": {"session_id": session_id, "client_id": client_id},
                "db": db,
            }
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
    return run_async(rotate_session_cookie_secret_async(session_id, **kwargs))


def bind_session_client(session_id, **kwargs):
    return run_async(bind_session_client_async(session_id, **kwargs))


async def persist_revoked_token_hash(
    db: Any,
    *,
    token_hash: str,
    token_type_hint: str | None = None,
    reason: str | None = None,
    subject: str | None = None,
    tenant_id: Any = None,
    client_id: Any = None,
    expires_at: Any = None,
) -> RevokedToken:
    return await RevokedToken.handlers.record_hash.core(
        {
            "payload": {
                "token_hash": token_hash,
                "token_type_hint": token_type_hint,
                "reason": reason,
                "subject": subject,
                "tenant_id": tenant_id,
                "client_id": client_id,
                "expires_at": expires_at,
            },
            "db": db,
        }
    )


async def revoke_token_async(token: str, token_type_hint: str | None = None, reason: str | None = None) -> str | None:
    if not settings.enable_rfc7009:
        return None
    digest = token_hash(token)
    now = datetime.now(timezone.utc)
    try:
        async with storage_session() as db:
            rows = _items(
                await TokenRecord.handlers.list.core(
                    {"payload": {"filters": {"token_hash": digest}}, "db": db}
                )
            )
            record = rows[0] if rows else None
            revoked_rows = _items(
                await RevokedToken.handlers.list.core(
                    {"payload": {"filters": {"token_hash": digest}}, "db": db}
                )
            )
            revoked = revoked_rows[0] if revoked_rows else None
            revoked_payload = {
                "token_hash": digest,
                "revoked_reason": reason or _field(revoked, "revoked_reason") or "revoked",
                "token_type_hint": token_type_hint or _field(revoked, "token_type_hint"),
            }
            if record is not None:
                await TokenRecord.handlers.update.core(
                    {
                        "path_params": {"id": _field(record, "id")},
                        "payload": {
                            "active": False,
                            "revoked_at": now,
                            "revoked_reason": reason or _field(record, "revoked_reason") or "revoked",
                        },
                        "db": db,
                    }
                )
                revoked_payload.update(
                    {
                        "subject": _field(record, "subject"),
                        "tenant_id": _field(record, "tenant_id"),
                        "client_id": _field(record, "client_id"),
                        "expires_at": _field(record, "expires_at"),
                        "token_type_hint": token_type_hint or _field(record, "token_type_hint"),
                    }
                )
            await persist_revoked_token_hash(
                db,
                token_hash=digest,
                token_type_hint=revoked_payload.get("token_type_hint"),
                reason=revoked_payload.get("revoked_reason"),
                subject=revoked_payload.get("subject"),
                tenant_id=revoked_payload.get("tenant_id"),
                client_id=revoked_payload.get("client_id"),
                expires_at=revoked_payload.get("expires_at"),
            )
    except Exception:
        return digest
    return digest


def revoke_token(token: str, token_type_hint: str | None = None, reason: str | None = None) -> str | None:
    if not settings.enable_rfc7009:
        return None
    return run_async(revoke_token_async(token, token_type_hint=token_type_hint, reason=reason))


async def is_token_revoked_async(token: str) -> bool:
    digest = token_hash(token)
    try:
        async with storage_session() as db:
            if await RevokedToken.handlers.is_hash_revoked.core({"payload": {"token_hash": digest}, "db": db}):
                return True
            rows = _items(
                await TokenRecord.handlers.list.core(
                    {"payload": {"filters": {"token_hash": digest}}, "db": db}
                )
            )
            record = rows[0] if rows else None
            if record is None:
                return False
            if _field(record, "revoked_at") is not None:
                return True
            expires_at = _field(record, "expires_at")
            if expires_at is not None:
                expiry = expires_at if expires_at.tzinfo is not None else expires_at.replace(tzinfo=timezone.utc)
                if expiry <= datetime.now(timezone.utc):
                    return True
            return not bool(_field(record, "active"))
    except Exception:
        return False


async def is_revoked_async(token: str) -> bool:
    if not settings.enable_rfc7009:
        return False
    return bool(await is_token_revoked_async(token))


def is_revoked(token: str) -> bool:
    if not settings.enable_rfc7009:
        return False
    return bool(run_async(is_token_revoked_async(token)))


is_token_revoked = is_revoked


async def reset_token_state_async() -> None:
    try:
        async with storage_session() as db:
            for model in (RevokedToken, TokenRecord):
                for row in await list_records(model, db):
                    await delete_record(model, db, record_id(row))
    except Exception:
        return None


async def reset_revocations_async() -> None:
    await reset_token_state_async()


def reset_token_state() -> None:
    run_async(reset_token_state_async())


def reset_revocations() -> None:
    run_async(reset_token_state_async())


from . import _persistence_extended as _extended
from ._persistence_extended import *  # noqa: F401,F403

__all__ = list(_extended.__all__)

