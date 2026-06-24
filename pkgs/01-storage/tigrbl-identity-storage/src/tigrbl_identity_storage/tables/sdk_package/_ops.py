from __future__ import annotations

__all__: list[str] = []

# BEGIN classmethod-to-op_ctx migration
from tigrbl import op_ctx as _table_op_ctx

from .._ops import create_record, first_record, record_id, update_record
from ._table import SDKPackageRecord
from typing import Any

@_table_op_ctx(bind=SDKPackageRecord, alias="register", target="custom", rest=False)
async def register(cls, db: Any, **payload: Any) -> "SDKPackageRecord":
    existing = await _lookup(cls, db, sdk_id=payload["sdk_id"])
    payload.setdefault("release_channel", "stable")
    payload.setdefault("contract_payload", dict(payload))
    payload.setdefault("status", "active")
    if existing is not None:
        return await update_record(cls, db, record_id(existing), payload)
    return await create_record(cls, db, payload)

async def _lookup(cls, db: Any, *, sdk_id: str) -> "SDKPackageRecord | None":
    return await first_record(cls, db, {"sdk_id": sdk_id})

@_table_op_ctx(bind=SDKPackageRecord, alias="disable", target="custom", rest=False)
async def disable(cls, db: Any, *, sdk_id: str) -> "SDKPackageRecord | None":
    row = await _lookup(cls, db, sdk_id=sdk_id)
    if row is None:
        return None
    return await update_record(cls, db, record_id(row), {"status": "disabled"})

# END classmethod-to-op_ctx migration
