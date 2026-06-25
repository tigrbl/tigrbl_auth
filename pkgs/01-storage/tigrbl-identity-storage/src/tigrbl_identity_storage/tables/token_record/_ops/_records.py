"""TokenRecord-owned lifecycle helpers formerly exposed by storage persistence."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from ..._ops import (
    delete_handler_record,
    field,
    first_handler_record,
    record_id,
    token_hash,
)
from ...engine import storage_session
from .._table import TokenRecord


async def upsert_token_record_async(
    token: str,
    claims: dict[str, Any] | None = None,
    *,
    token_kind: str | None = None,
    token_type_hint: str | None = None,
    refresh_family_id: str | None = None,
    refresh_parent_hash: str | None = None,
    refresh_successor_hash: str | None = None,
    used_at: datetime | None = None,
    reuse_detected_at: datetime | None = None,
) -> str:
    claims = dict(claims or {})
    digest = token_hash(token)
    token_kind = token_kind or str(claims.get("kind") or claims.get("typ") or "access")
    try:
        async with storage_session() as db:
            await TokenRecord.handlers.persist_issued.core(
                {
                    "payload": {
                        "token_hash": digest,
                        "claims": claims,
                        "token_kind": token_kind,
                        "token_type_hint": token_type_hint or token_kind,
                        "refresh_family_id": refresh_family_id,
                        "refresh_parent_hash": refresh_parent_hash,
                        "refresh_successor_hash": refresh_successor_hash,
                        "issued_at": datetime.now(timezone.utc),
                        "used_at": used_at,
                        "reuse_detected_at": reuse_detected_at,
                    },
                    "db": db,
                }
            )
    except Exception:
        return digest
    return digest


async def remove_token_record_async(token: str) -> None:
    digest = token_hash(token)
    try:
        async with storage_session() as db:
            record = await first_handler_record(TokenRecord, db, {"token_hash": digest})
            if record is not None:
                await delete_handler_record(TokenRecord, db, record_id(record))
    except Exception:
        return None


async def get_token_record_async(token: str) -> TokenRecord | None:
    digest = token_hash(token)
    try:
        async with storage_session() as db:
            return await first_handler_record(TokenRecord, db, {"token_hash": digest})
    except Exception:
        return None


async def mark_token_used_async(
    token: str,
    *,
    successor_token: str | None = None,
    reason: str = "refresh_rotated",
) -> str:
    digest = token_hash(token)
    successor_hash = token_hash(successor_token) if successor_token else None
    try:
        async with storage_session() as db:
            await TokenRecord.handlers.mark_rotated.core(
                {"payload": {"token_hash": digest, "successor_hash": successor_hash, "reason": reason}, "db": db}
            )
    except Exception:
        return digest
    return digest


async def revoke_refresh_family_async(
    family_id: str,
    *,
    reason: str = "refresh_token_reuse_detected",
    reuse_token: str | None = None,
) -> int:
    if not family_id:
        return 0
    from ...revoked_token._table import RevokedToken

    reuse_hash = token_hash(reuse_token) if reuse_token else None
    revoked_count = 0
    try:
        async with storage_session() as db:
            rows = await TokenRecord.handlers.revoke_family.core(
                {
                    "payload": {"refresh_family_id": family_id, "reason": reason, "reuse_token_hash": reuse_hash},
                    "db": db,
                }
            )
            for row in rows:
                token_record_hash = field(row, "token_hash")
                await RevokedToken.handlers.record_hash.core(
                    {
                        "payload": {
                            "token_hash": token_record_hash,
                            "token_type_hint": field(row, "token_type_hint"),
                            "reason": reason,
                            "subject": field(row, "subject"),
                            "tenant_id": field(row, "tenant_id"),
                            "client_id": field(row, "client_id"),
                            "expires_at": field(row, "expires_at"),
                        },
                        "db": db,
                    }
                )
                revoked_count += 1
    except Exception:
        return 0
    return revoked_count


__all__ = [
    "get_token_record_async",
    "mark_token_used_async",
    "remove_token_record_async",
    "revoke_refresh_family_async",
    "token_hash",
    "upsert_token_record_async",
]
