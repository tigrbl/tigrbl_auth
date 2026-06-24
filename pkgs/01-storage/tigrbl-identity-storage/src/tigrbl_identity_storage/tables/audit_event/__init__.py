from __future__ import annotations

from . import _table as _table
from ._table import *
from ..engine import storage_session
from ..tenant._table import Tenant


def _created_item(result):
    if isinstance(result, dict):
        for key in ("item", "result", "data"):
            if key in result:
                return result[key]
    return result


def _list_items(result):
    if isinstance(result, dict) and isinstance(result.get("items"), list):
        return result["items"]
    if hasattr(result, "items"):
        result = result.items
    if isinstance(result, list):
        return result
    if isinstance(result, tuple):
        return list(result)
    if result is None:
        return []
    return [result]


async def append_audit_event_async(**kwargs):
    async with storage_session() as db:
        payload = dict(kwargs)
        if payload.get("tenant_id") is None:
            tenants = await Tenant.handlers.list.core({"payload": {"filters": {}}, "db": db})
            tenant_rows = _list_items(tenants)
            if tenant_rows:
                payload["tenant_id"] = getattr(tenant_rows[0], "id", None)
        row = await AuditEvent.handlers.create.core({"payload": payload, "db": db})
        return _created_item(row)


def append_audit_event(**kwargs):
    return _table.run_async(append_audit_event_async(**kwargs))


try:
    __all__ = list(_table.__all__)
except AttributeError:
    __all__ = [name for name in globals() if not name.startswith("_")]
__all__ += ["append_audit_event", "append_audit_event_async"]
