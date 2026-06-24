from __future__ import annotations

__all__: list[str] = []

# BEGIN classmethod-to-op_ctx migration
from tigrbl import op_ctx as _table_op_ctx
from . import _table as _table_module

for _table_name in dir(_table_module):
    if not _table_name.startswith("__"):
        globals().setdefault(_table_name, getattr(_table_module, _table_name))

@_table_op_ctx(bind=ScimUserRecord, alias="upsert_user", target="custom", rest=False)
async def upsert_user(cls, db: Any, **payload: Any) -> "ScimUserRecord":
    existing = await _lookup(cls, db, user_id=payload["user_id"])
    payload.setdefault("status", "active" if payload.get("active", True) else "disabled")
    if existing is not None:
        return await update_record(cls, db, record_id(existing), payload)
    return await create_record(cls, db, payload)

async def _lookup(cls, db: Any, *, user_id: str) -> "ScimUserRecord | None":
    return await first_record(cls, db, {"user_id": user_id})

@_table_op_ctx(bind=ScimUserRecord, alias="deactivate", target="custom", rest=False)
async def deactivate(cls, db: Any, *, user_id: str) -> "ScimUserRecord | None":
    row = await _lookup(cls, db, user_id=user_id)
    if row is None:
        return None
    return await update_record(cls, db, record_id(row), {"status": "disabled"})

# END classmethod-to-op_ctx migration
