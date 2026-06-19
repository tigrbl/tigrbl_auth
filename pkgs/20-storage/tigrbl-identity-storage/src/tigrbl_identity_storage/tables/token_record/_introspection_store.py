"""TokenRecord-owned durable introspection helpers."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from .._ops import field, first_handler_record, record_id, token_hash, update_handler_record
from .._session import storage_session
from ..revoked_token._table import RevokedToken
from ._table import TokenRecord


async def introspect_token_record_async(token: str) -> dict[str, Any]:
    digest = token_hash(token)
    now = datetime.now(timezone.utc)
    try:
        async with storage_session() as db:
            record = await first_handler_record(TokenRecord, db, {"token_hash": digest})
            if record is None:
                return {"active": False}
            expires_at = field(record, "expires_at")
            if expires_at is not None:
                expiry = expires_at if expires_at.tzinfo is not None else expires_at.replace(tzinfo=timezone.utc)
                if expiry <= now:
                    await update_handler_record(
                        TokenRecord,
                        db,
                        record_id(record),
                        {"active": False, "revoked_reason": field(record, "revoked_reason") or "expired"},
                    )
                    return {"active": False}
            revoked = await first_handler_record(RevokedToken, db, {"token_hash": digest})
            if revoked is not None or field(record, "revoked_at") is not None or not field(record, "active"):
                await update_handler_record(
                    TokenRecord,
                    db,
                    record_id(record),
                    {"active": False, "last_introspected_at": now},
                )
                return {"active": False}
            await update_handler_record(TokenRecord, db, record_id(record), {"last_introspected_at": now})
            payload = dict(field(record, "claims") or {})
            payload.setdefault("sub", field(record, "subject"))
            if field(record, "scope"):
                payload.setdefault("scope", field(record, "scope"))
            if field(record, "client_id") is not None:
                payload.setdefault("client_id", str(field(record, "client_id")))
            if field(record, "issuer"):
                payload.setdefault("iss", field(record, "issuer"))
            if expires_at is not None:
                payload.setdefault("exp", int(expires_at.timestamp()))
            payload["active"] = True
            return payload
    except Exception:
        return {"active": False}


__all__ = ["introspect_token_record_async"]
