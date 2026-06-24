from __future__ import annotations

__all__: list[str] = []

# BEGIN classmethod-to-op_ctx migration
from tigrbl import op_ctx as _table_op_ctx
from . import _table as _table_module

for _table_name in dir(_table_module):
    if not _table_name.startswith("__"):
        globals().setdefault(_table_name, getattr(_table_module, _table_name))

@_table_op_ctx(bind=ResourceServerContract, alias="register", target="custom", rest=False)
async def register(cls, db: Any, **payload: Any) -> "ResourceServerContract":
    existing = await _lookup(cls, db, contract_id=payload["contract_id"])
    payload.setdefault("contract_payload", dict(payload))
    payload.setdefault("status", "active")
    if existing is not None:
        return await update_record(cls, db, record_id(existing), payload)
    return await create_record(cls, db, payload)

async def _lookup(cls, db: Any, *, contract_id: str) -> "ResourceServerContract | None":
    return await first_record(cls, db, {"contract_id": contract_id})

@_table_op_ctx(bind=ResourceServerContract, alias="disable", target="custom", rest=False)
async def disable(cls, db: Any, *, contract_id: str) -> "ResourceServerContract | None":
    row = await _lookup(cls, db, contract_id=contract_id)
    if row is None:
        return None
    return await update_record(cls, db, record_id(row), {"status": "disabled"})

# END classmethod-to-op_ctx migration
