from __future__ import annotations

__all__: list[str] = []

# BEGIN classmethod-to-op_ctx migration
from tigrbl import op_ctx as _table_op_ctx
from . import _table as _table_module

for _table_name in dir(_table_module):
    if not _table_name.startswith("__"):
        globals().setdefault(_table_name, getattr(_table_module, _table_name))

@_table_op_ctx(bind=EntitlementAssignment, alias="assign", target="custom", rest=False)
async def assign(cls, db: Any, **payload: Any) -> "EntitlementAssignment":
    payload.setdefault("status", "active")
    return await create_record(cls, db, payload)

async def _lookup(cls, db: Any, *, assignment_id: str) -> "EntitlementAssignment | None":
    return await first_record(cls, db, {"assignment_id": assignment_id})

@_table_op_ctx(bind=EntitlementAssignment, alias="revoke", target="custom", rest=False)
async def revoke(cls, db: Any, *, assignment_id: str, reason: str) -> "EntitlementAssignment | None":
    row = await _lookup(cls, db, assignment_id=assignment_id)
    if row is None:
        return None
    return await update_record(
        cls,
        db,
        record_id(row),
        {"status": "revoked", "revoked_reason": reason},
    )

# END classmethod-to-op_ctx migration
