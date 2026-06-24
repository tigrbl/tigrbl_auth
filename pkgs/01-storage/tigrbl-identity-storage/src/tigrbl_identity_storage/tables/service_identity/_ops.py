from __future__ import annotations

__all__: list[str] = []

# BEGIN classmethod-to-op_ctx migration
from tigrbl import op_ctx as _table_op_ctx
from . import _table as _table_module

for _table_name in dir(_table_module):
    if not _table_name.startswith("__"):
        globals().setdefault(_table_name, getattr(_table_module, _table_name))

async def _lookup(cls, db: Any, *, service_identity_id: Any) -> "ServiceIdentity | None":
    return await first_record(cls, db, {"id": service_identity_id})

@_table_op_ctx(bind=ServiceIdentity, alias="disable", target="custom", rest=False)
async def disable(cls, db: Any, *, service_identity_id: Any) -> "ServiceIdentity | None":
    row = await _lookup(cls, db, service_identity_id=service_identity_id)
    if row is None:
        return None
    return await update_record(cls, db, record_id(row), {"is_active": False})

# END classmethod-to-op_ctx migration
