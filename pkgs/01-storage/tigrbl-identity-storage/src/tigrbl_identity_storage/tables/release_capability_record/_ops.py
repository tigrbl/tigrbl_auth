from __future__ import annotations

__all__: list[str] = []

# BEGIN classmethod-to-op_ctx migration
from tigrbl import op_ctx as _table_op_ctx

from .._ops import create_record, first_record, record_id, update_record
from ._table import ReleaseCapabilityRecord
from typing import Any

@_table_op_ctx(bind=ReleaseCapabilityRecord, alias="record", target="custom", rest=False)
async def record(cls, db: Any, **payload: Any) -> "ReleaseCapabilityRecord":
    existing = await _lookup(cls, db, capability_id=payload["capability_id"])
    payload.setdefault("capability_payload", dict(payload))
    payload.setdefault("status", "recorded")
    if existing is not None:
        return await update_record(cls, db, record_id(existing), payload)
    return await create_record(cls, db, payload)

async def _lookup(cls, db: Any, *, capability_id: str) -> "ReleaseCapabilityRecord | None":
    return await first_record(cls, db, {"capability_id": capability_id})

# END classmethod-to-op_ctx migration
