from __future__ import annotations

__all__: list[str] = []

# BEGIN classmethod-to-op_ctx migration
from tigrbl import op_ctx as _table_op_ctx
from . import _table as _table_module

for _table_name in dir(_table_module):
    if not _table_name.startswith("__"):
        globals().setdefault(_table_name, getattr(_table_module, _table_name))

@_table_op_ctx(bind=Realm, alias="update_realm", target="custom", rest=False)
async def update_realm(cls, db: Any, *, realm_id: uuid.UUID, **payload: Any) -> "Realm | None":
    row = await first_record(cls, db, {"id": realm_id})
    if row is None:
        return None
    return await update_record(cls, db, record_id(row), payload)

# END classmethod-to-op_ctx migration
