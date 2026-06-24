from __future__ import annotations

__all__: list[str] = []

# BEGIN classmethod-to-op_ctx migration
from tigrbl import op_ctx as _table_op_ctx
from . import _table as _table_module

for _table_name in dir(_table_module):
    if not _table_name.startswith("__"):
        globals().setdefault(_table_name, getattr(_table_module, _table_name))

@_table_op_ctx(bind=TenantMembership, alias="grant_membership", target="custom", rest=False)
async def grant_membership(
    cls,
    db: Any,
    *,
    tenant_id: str,
    principal_id: str,
    roles: list[str] | tuple[str, ...] = (),
    status: str = "active",
) -> "TenantMembership":
    existing = await _lookup(cls, db, tenant_id=tenant_id, principal_id=principal_id)
    payload = {"tenant_id": tenant_id, "principal_id": principal_id, "roles": list(roles), "status": status}
    if existing is not None:
        return await update_record(cls, db, record_id(existing), payload)
    return await create_record(cls, db, payload)

async def _lookup(cls, db: Any, *, tenant_id: str, principal_id: str) -> "TenantMembership | None":
    return await first_record(cls, db, {"tenant_id": tenant_id, "principal_id": principal_id})

async def _list_for_principal(cls, db: Any, *, principal_id: str) -> list["TenantMembership"]:
    return await list_records(cls, db, {"principal_id": principal_id})

@_table_op_ctx(bind=TenantMembership, alias="assign_role", target="custom", rest=False)
async def assign_role(
    cls,
    db: Any,
    *,
    tenant_id: str,
    principal_id: str,
    role_name: str,
) -> "TenantMembership":
    membership = await _lookup(cls, db, tenant_id=tenant_id, principal_id=principal_id)
    roles = set(_str_tuple(getattr(membership, "roles", None) if membership is not None else ()))
    if isinstance(membership, dict):
        roles = set(_str_tuple(membership.get("roles")))
    roles.add(role_name)
    return await cls.grant_membership(
        db,
        tenant_id=tenant_id,
        principal_id=principal_id,
        roles=tuple(sorted(roles)),
    )

@_table_op_ctx(bind=TenantMembership, alias="role_names_for_principal", target="custom", rest=False)
async def role_names_for_principal(
    cls,
    db: Any,
    *,
    principal_id: str,
    tenant_id: str | None = None,
) -> tuple[str, ...]:
    roles: set[str] = set()
    for row in await _list_for_principal(cls, db, principal_id=principal_id):
        row_status = row.get("status", "active") if isinstance(row, dict) else getattr(row, "status", "active")
        if str(row_status or "active") != "active":
            continue
        row_tenant_id = row.get("tenant_id") if isinstance(row, dict) else getattr(row, "tenant_id", None)
        if tenant_id is not None and row_tenant_id != tenant_id:
            continue
        row_roles = row.get("roles") if isinstance(row, dict) else getattr(row, "roles", None)
        roles.update(_str_tuple(row_roles))
    return tuple(sorted(roles))

@_table_op_ctx(bind=TenantMembership, alias="revoke_membership", target="custom", rest=False)
async def revoke_membership(cls, db: Any, *, tenant_id: str, principal_id: str) -> "TenantMembership | None":
    row = await _lookup(cls, db, tenant_id=tenant_id, principal_id=principal_id)
    if row is None:
        return None
    return await update_record(cls, db, record_id(row), {"status": "revoked"})

# END classmethod-to-op_ctx migration
