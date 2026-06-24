from __future__ import annotations

__all__: list[str] = []

# BEGIN classmethod-to-op_ctx migration
from tigrbl import op_ctx as _table_op_ctx
from . import _table as _table_module

for _table_name in dir(_table_module):
    if not _table_name.startswith("__"):
        globals().setdefault(_table_name, getattr(_table_module, _table_name))

@_table_op_ctx(bind=Role, alias="create_role", target="custom", rest=False)
async def create_role(
    cls,
    db: Any,
    *,
    name: str,
    permissions: list[str] | tuple[str, ...],
    tenant_id: str | None = None,
    denied_permissions: list[str] | tuple[str, ...] = (),
    inherited_roles: list[str] | tuple[str, ...] = (),
) -> "Role":
    existing = await _lookup(cls, db, name=name, tenant_id=tenant_id)
    payload = {
        "name": name,
        "tenant_id": tenant_id,
        "permissions": list(permissions),
        "denied_permissions": list(denied_permissions),
        "inherited_roles": list(inherited_roles),
        "status": "active",
    }
    if existing is not None:
        return await update_record(cls, db, record_id(existing), payload)
    return await create_record(cls, db, payload)

async def _lookup(cls, db: Any, *, name: str, tenant_id: str | None = None) -> "Role | None":
    filters: dict[str, Any] = {"name": name}
    if tenant_id is not None:
        filters["tenant_id"] = tenant_id
    return await first_record(cls, db, filters)

@_table_op_ctx(bind=Role, alias="disable", target="custom", rest=False)
async def disable(cls, db: Any, *, name: str, tenant_id: str | None = None) -> "Role | None":
    row = await _lookup(cls, db, name=name, tenant_id=tenant_id)
    if row is None:
        return None
    return await update_record(cls, db, record_id(row), {"status": "disabled"})

# END classmethod-to-op_ctx migration
