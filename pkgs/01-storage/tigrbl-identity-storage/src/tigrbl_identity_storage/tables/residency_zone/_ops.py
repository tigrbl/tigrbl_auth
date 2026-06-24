from __future__ import annotations

__all__: list[str] = []

# BEGIN classmethod-to-op_ctx migration
from tigrbl import op_ctx as _table_op_ctx

from .._ops import first_record, record_id, update_record
from ._table import ResidencyZone
from typing import Any

async def _lookup(cls, db: Any, *, zone_id: str) -> "ResidencyZone | None":
    return await first_record(cls, db, {"zone_id": zone_id})

@_table_op_ctx(bind=ResidencyZone, alias="disable", target="custom", rest=False)
async def disable(cls, db: Any, *, zone_id: str) -> "ResidencyZone | None":
    row = await _lookup(cls, db, zone_id=zone_id)
    if row is None:
        return None
    return await update_record(cls, db, record_id(row), {"status": "disabled"})

# END classmethod-to-op_ctx migration
