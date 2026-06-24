from __future__ import annotations

__all__: list[str] = []

# BEGIN classmethod-to-op_ctx migration
from tigrbl import op_ctx as _table_op_ctx

from .._ops import create_record, first_record, record_id, update_record
from ._table import ScimSchemaRecord
from typing import Any

@_table_op_ctx(bind=ScimSchemaRecord, alias="register_schema", target="custom", rest=False)
async def register_schema(cls, db: Any, **payload: Any) -> "ScimSchemaRecord":
    existing = await _lookup(cls, db, schema_id=payload["schema_id"])
    payload.setdefault("schema_payload", dict(payload))
    payload.setdefault("status", "active")
    if existing is not None:
        return await update_record(cls, db, record_id(existing), payload)
    return await create_record(cls, db, payload)

async def _lookup(cls, db: Any, *, schema_id: str) -> "ScimSchemaRecord | None":
    return await first_record(cls, db, {"schema_id": schema_id})

@_table_op_ctx(bind=ScimSchemaRecord, alias="disable", target="custom", rest=False)
async def disable(cls, db: Any, *, schema_id: str) -> "ScimSchemaRecord | None":
    row = await _lookup(cls, db, schema_id=schema_id)
    if row is None:
        return None
    return await update_record(cls, db, record_id(row), {"status": "disabled"})

# END classmethod-to-op_ctx migration
