from __future__ import annotations

__all__: list[str] = []

# BEGIN classmethod-to-op_ctx migration
from tigrbl import op_ctx as _table_op_ctx

from .._ops import create_record, first_record, record_id, update_record
from ._table import PluginDescriptorRecord
from typing import Any

@_table_op_ctx(bind=PluginDescriptorRecord, alias="register", target="custom", rest=False)
async def register(cls, db: Any, **payload: Any) -> "PluginDescriptorRecord":
    existing = await _lookup(cls, db, plugin_id=payload["plugin_id"])
    payload.setdefault("descriptor_payload", dict(payload))
    payload.setdefault("status", "enabled" if payload.get("enabled", True) else "disabled")
    if existing is not None:
        return await update_record(cls, db, record_id(existing), payload)
    return await create_record(cls, db, payload)

async def _lookup(cls, db: Any, *, plugin_id: str) -> "PluginDescriptorRecord | None":
    return await first_record(cls, db, {"plugin_id": plugin_id})

@_table_op_ctx(bind=PluginDescriptorRecord, alias="disable", target="custom", rest=False)
async def disable(cls, db: Any, *, plugin_id: str) -> "PluginDescriptorRecord | None":
    row = await _lookup(cls, db, plugin_id=plugin_id)
    if row is None:
        return None
    return await update_record(cls, db, record_id(row), {"status": "disabled"})

# END classmethod-to-op_ctx migration
