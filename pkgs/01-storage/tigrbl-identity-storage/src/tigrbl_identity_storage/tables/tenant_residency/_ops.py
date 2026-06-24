from __future__ import annotations

__all__: list[str] = []

# BEGIN classmethod-to-op_ctx migration
from tigrbl import op_ctx as _table_op_ctx

from .._ops import create_record, first_record, record_id, update_record
from ._table import TenantResidency
from typing import Any

@_table_op_ctx(bind=TenantResidency, alias="assign_residency", target="custom", rest=False)
async def assign_residency(cls, db: Any, **payload: Any) -> "TenantResidency":
    existing = await _lookup(cls, db, tenant_id=payload["tenant_id"])
    payload.setdefault("status", "active")
    if existing is not None:
        return await update_record(cls, db, record_id(existing), payload)
    return await create_record(cls, db, payload)

async def _lookup(cls, db: Any, *, tenant_id: str) -> "TenantResidency | None":
    return await first_record(cls, db, {"tenant_id": tenant_id})

@_table_op_ctx(bind=TenantResidency, alias="disable", target="custom", rest=False)
async def disable(cls, db: Any, *, tenant_id: str) -> "TenantResidency | None":
    row = await _lookup(cls, db, tenant_id=tenant_id)
    if row is None:
        return None
    return await update_record(cls, db, record_id(row), {"status": "disabled"})

# END classmethod-to-op_ctx migration
