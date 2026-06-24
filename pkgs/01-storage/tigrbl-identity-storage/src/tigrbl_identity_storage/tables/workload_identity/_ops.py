from __future__ import annotations

# BEGIN classmethod-to-op_ctx migration
from tigrbl import op_ctx as _table_op_ctx

from .._ops import first_record, record_id, update_record
from ._table import WorkloadIdentity
from typing import Any

async def _lookup(cls, db: Any, *, principal_id: str) -> "WorkloadIdentity | None":
    return await first_record(cls, db, {"principal_id": principal_id})

@_table_op_ctx(bind=WorkloadIdentity, alias="disable", target="custom", rest=False)
async def disable(cls, db: Any, *, principal_id: str) -> "WorkloadIdentity | None":
    row = await _lookup(cls, db, principal_id=principal_id)
    if row is None:
        return None
    return await update_record(cls, db, record_id(row), {"status": "disabled"})

# END classmethod-to-op_ctx migration
