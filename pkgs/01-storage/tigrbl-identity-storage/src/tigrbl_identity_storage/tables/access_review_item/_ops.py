from __future__ import annotations

__all__: list[str] = []

# BEGIN classmethod-to-op_ctx migration
from tigrbl import op_ctx as _table_op_ctx
from . import _table as _table_module

for _table_name in dir(_table_module):
    if not _table_name.startswith("__"):
        globals().setdefault(_table_name, getattr(_table_module, _table_name))

async def _lookup(cls, db: Any, *, item_id: str) -> "AccessReviewItem | None":
    return await first_record(cls, db, {"item_id": item_id})

@_table_op_ctx(bind=AccessReviewItem, alias="mark_decided", target="custom", rest=False)
async def mark_decided(cls, db: Any, *, item_id: str) -> "AccessReviewItem | None":
    row = await _lookup(cls, db, item_id=item_id)
    if row is None:
        return None
    return await update_record(cls, db, record_id(row), {"status": "decided"})

# END classmethod-to-op_ctx migration
