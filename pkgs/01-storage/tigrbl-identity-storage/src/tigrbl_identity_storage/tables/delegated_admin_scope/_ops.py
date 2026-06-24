from __future__ import annotations

__all__: list[str] = []

# BEGIN classmethod-to-op_ctx migration
from tigrbl import op_ctx as _table_op_ctx
from . import _table as _table_module

for _table_name in dir(_table_module):
    if not _table_name.startswith("__"):
        globals().setdefault(_table_name, getattr(_table_module, _table_name))

@_table_op_ctx(bind=DelegatedAdminScope, alias="grant_scope", target="custom", rest=False)
async def grant_scope(cls, db: Any, **payload: Any) -> "DelegatedAdminScope":
    existing = await _lookup(cls, db, subject=payload["subject"])
    payload.setdefault("status", "active")
    if existing is not None:
        return await update_record(cls, db, record_id(existing), payload)
    return await create_record(cls, db, payload)

async def _lookup(cls, db: Any, *, subject: str) -> "DelegatedAdminScope | None":
    return await first_record(cls, db, {"subject": subject})

@_table_op_ctx(bind=DelegatedAdminScope, alias="revoke_scope", target="custom", rest=False)
async def revoke_scope(cls, db: Any, *, subject: str) -> "DelegatedAdminScope | None":
    row = await _lookup(cls, db, subject=subject)
    if row is None:
        return None
    return await update_record(cls, db, record_id(row), {"status": "revoked"})

# END classmethod-to-op_ctx migration
