from __future__ import annotations

__all__: list[str] = []

# BEGIN classmethod-to-op_ctx migration
from tigrbl import op_ctx as _table_op_ctx

from .._ops import create_record, first_record, record_id, update_record
from ._table import Entitlement
from typing import Any

@_table_op_ctx(bind=Entitlement, alias="define", target="custom", rest=False)
async def define(cls, db: Any, **payload: Any) -> "Entitlement":
    existing = await _lookup(cls, db, entitlement_id=payload["entitlement_id"])
    payload.setdefault("status", "active")
    if existing is not None:
        return await update_record(cls, db, record_id(existing), payload)
    return await create_record(cls, db, payload)

async def _lookup(cls, db: Any, *, entitlement_id: str) -> "Entitlement | None":
    return await first_record(cls, db, {"entitlement_id": entitlement_id})

@_table_op_ctx(bind=Entitlement, alias="disable", target="custom", rest=False)
async def disable(cls, db: Any, *, entitlement_id: str) -> "Entitlement | None":
    row = await _lookup(cls, db, entitlement_id=entitlement_id)
    if row is None:
        return None
    return await update_record(cls, db, record_id(row), {"status": "disabled"})

# END classmethod-to-op_ctx migration
