from __future__ import annotations

__all__: list[str] = []

# BEGIN classmethod-to-op_ctx migration
from tigrbl import op_ctx as _table_op_ctx

from .._ops import first_record, record_id, update_record, utc_now
from ._table import KeyRotationPolicy
from typing import Any

async def _lookup_version(cls, db: Any, *, version_id: str) -> "KeyRotationPolicy | None":
    return await first_record(cls, db, {"version_id": version_id})

@_table_op_ctx(bind=KeyRotationPolicy, alias="approve", target="custom", rest=False)
async def approve(cls, db: Any, *, version_id: str, approved_by: str) -> "KeyRotationPolicy | None":
    row = await _lookup_version(cls, db, version_id=version_id)
    if row is None:
        return None
    return await update_record(
        cls,
        db,
        record_id(row),
        {"status": "approved", "approved_by": approved_by, "approved_at": utc_now()},
    )

@_table_op_ctx(bind=KeyRotationPolicy, alias="publish", target="custom", rest=False)
async def publish(cls, db: Any, *, version_id: str) -> "KeyRotationPolicy | None":
    row = await _lookup_version(cls, db, version_id=version_id)
    if row is None:
        return None
    return await update_record(cls, db, record_id(row), {"status": "published", "published_at": utc_now()})

# END classmethod-to-op_ctx migration
