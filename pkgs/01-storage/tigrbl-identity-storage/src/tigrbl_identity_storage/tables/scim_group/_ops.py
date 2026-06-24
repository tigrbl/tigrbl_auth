from __future__ import annotations

__all__: list[str] = []

# BEGIN classmethod-to-op_ctx migration
from tigrbl import op_ctx as _table_op_ctx

from .._ops import create_record, first_record, record_id, update_record
from ._table import ScimGroupRecord
from typing import Any

@_table_op_ctx(bind=ScimGroupRecord, alias="upsert_group", target="custom", rest=False)
async def upsert_group(cls, db: Any, **payload: Any) -> "ScimGroupRecord":
    existing = await _lookup(cls, db, group_id=payload["group_id"])
    payload.setdefault("status", "active")
    if existing is not None:
        return await update_record(cls, db, record_id(existing), payload)
    return await create_record(cls, db, payload)

async def _lookup(cls, db: Any, *, group_id: str) -> "ScimGroupRecord | None":
    return await first_record(cls, db, {"group_id": group_id})

@_table_op_ctx(bind=ScimGroupRecord, alias="deactivate", target="custom", rest=False)
async def deactivate(cls, db: Any, *, group_id: str) -> "ScimGroupRecord | None":
    row = await _lookup(cls, db, group_id=group_id)
    if row is None:
        return None
    return await update_record(cls, db, record_id(row), {"status": "disabled"})

# END classmethod-to-op_ctx migration
