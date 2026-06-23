"""Domain-organized OAuth 2.0 token revocation support backed by durable persistence."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from typing import Final

from tigrbl_identity_runtime.settings import settings
from .._ops import (
    clear_handler_records,
    field,
    first_handler_record,
    record_id,
    token_hash,
    update_handler_record,
)
from .._session import storage_session
from .._sync import run_async
from ..token_record._table import TokenRecord
from ._table import RevokedToken

RFC7009_SPEC_URL: Final[str] = "https://www.rfc-editor.org/rfc/rfc7009"
CANONICAL_REVOCATION_PATH: Final[str] = "/revoke"


def revoke_token(token: str, token_type_hint: str | None = None, reason: str | None = None) -> str | None:
    if not settings.enable_rfc7009:
        return None
    return run_async(revoke_token_async(token, token_type_hint=token_type_hint, reason=reason))


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
    return await RevokedToken.revoke_token(
        db,
        token_hash=token_hash,
        token_type_hint=token_type_hint,
        reason=reason,
        subject=subject,
        tenant_id=tenant_id,
        client_id=client_id,
        expires_at=expires_at,
    )


async def revoke_token_async(token: str, token_type_hint: str | None = None, reason: str | None = None) -> str | None:
    if not settings.enable_rfc7009:
        return None
    digest = token_hash(token)
    now = datetime.now(timezone.utc)
    try:
        async with storage_session() as db:
            record = await first_handler_record(TokenRecord, db, {"token_hash": digest})
            revoked = await first_handler_record(RevokedToken, db, {"token_hash": digest})
            revoked_payload = {
                "token_hash": digest,
                "revoked_reason": reason or field(revoked, "revoked_reason") or "revoked",
                "token_type_hint": token_type_hint or field(revoked, "token_type_hint"),
            }
            if record is not None:
                await update_handler_record(
                    TokenRecord,
                    db,
                    record_id(record),
                    {
                        "active": False,
                        "revoked_at": now,
                        "revoked_reason": reason or field(record, "revoked_reason") or "revoked",
                    },
                )
                revoked_payload.update(
                    {
                        "subject": field(record, "subject"),
                        "tenant_id": field(record, "tenant_id"),
                        "client_id": field(record, "client_id"),
                        "expires_at": field(record, "expires_at"),
                        "token_type_hint": token_type_hint or field(record, "token_type_hint"),
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


def is_revoked(token: str) -> bool:
    if not settings.enable_rfc7009:
        return False
    return bool(run_async(is_token_revoked_async(token)))


async def is_revoked_async(token: str) -> bool:
    if not settings.enable_rfc7009:
        return False
    return bool(await is_token_revoked_async(token))


async def is_token_revoked_async(token: str) -> bool:
    digest = token_hash(token)
    try:
        async with storage_session() as db:
            if await RevokedToken.is_revoked(db, token_hash=digest):
                return True
            record = await first_handler_record(TokenRecord, db, {"token_hash": digest})
            if record is None:
                return False
            if field(record, "revoked_at") is not None:
                return True
            expires_at = field(record, "expires_at")
            if expires_at is not None:
                expiry = expires_at if expires_at.tzinfo is not None else expires_at.replace(tzinfo=timezone.utc)
                if expiry <= datetime.now(timezone.utc):
                    return True
            return not bool(field(record, "active"))
    except Exception:
        return False


is_token_revoked = is_revoked


def reset_revocations() -> None:
    run_async(reset_token_state_async())


async def reset_revocations_async() -> None:
    await reset_token_state_async()


async def reset_token_state_async() -> None:
    try:
        async with storage_session() as db:
            await clear_handler_records(RevokedToken, db)
            await clear_handler_records(TokenRecord, db)
    except Exception:
        return None


def reset_token_state() -> None:
    run_async(reset_token_state_async())


__all__ = [
    "RFC7009_SPEC_URL",
    "CANONICAL_REVOCATION_PATH",
    "revoke_token",
    "revoke_token_async",
    "persist_revoked_token_hash",
    "is_revoked",
    "is_revoked_async",
    "is_token_revoked",
    "is_token_revoked_async",
    "reset_revocations",
    "reset_revocations_async",
    "reset_token_state",
    "reset_token_state_async",
]
