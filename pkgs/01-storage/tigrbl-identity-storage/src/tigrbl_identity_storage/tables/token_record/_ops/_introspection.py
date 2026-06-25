"""TokenRecord-owned durable introspection helpers."""

from __future__ import annotations

from typing import Any

from ..._ops import token_hash
from ...engine import storage_session
from ...revoked_token._table import RevokedToken
from .._table import TokenRecord


async def introspect_token_record_async(token: str) -> dict[str, Any]:
    digest = token_hash(token)
    try:
        async with storage_session() as db:
            revoked = await RevokedToken.handlers.is_hash_revoked.core({"payload": {"token_hash": digest}, "db": db})
            if revoked:
                return {"active": False}
            return await TokenRecord.handlers.introspect_record.core({"payload": {"token_hash": digest}, "db": db})
    except Exception:
        return {"active": False}


__all__ = ["introspect_token_record_async"]
