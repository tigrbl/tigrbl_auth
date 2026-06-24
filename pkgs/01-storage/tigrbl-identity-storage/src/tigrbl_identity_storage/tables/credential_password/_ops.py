from __future__ import annotations

# BEGIN classmethod-to-op_ctx migration
from tigrbl import op_ctx as _table_op_ctx
from . import _table as _table_module

for _table_name in dir(_table_module):
    if not _table_name.startswith("__"):
        globals().setdefault(_table_name, getattr(_table_module, _table_name))

@_table_op_ctx(bind=CredentialPassword, alias="revoke", target="custom", rest=False)
async def revoke(cls, db: Any, *, credential_id: str) -> "CredentialPassword | None":
    row = await first_record(cls, db, {"credential_id": credential_id})
    if row is None:
        return None
    return await update_record(cls, db, record_id(row), {"status": "revoked"})

# END classmethod-to-op_ctx migration
