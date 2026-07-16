"""Durable runtime composition for tenant-administration capability calls."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from tigrbl_identity_server.admin_bootstrap import resolve_admin_user_from_request
from tigrbl_tenant_administration_capability import TenantAdministrationCapability
from tigrbl_identity_contracts.admin_tenants import (
    AdminTenant,
    AdminTenantCreate,
    AdminTenantUpdate,
    TenantAdministrationConflictError,
    TenantAdministrationNotFoundError,
    TenantAdministrationValidationError,
    TenantAdministrator,
    TenantAdministratorAuthenticationError,
)
from tigrbl_identity_storage.tables import Tenant
from tigrbl_identity_storage_runtime.engine import get_db
from tigrbl_identity_storage_runtime.ops.common import (
    create_table_record,
    delete_table_record,
    field_value,
    first_table_record,
    list_table_records,
    read_table_record,
    update_table_record,
)


def _uuid(value: str, *, label: str) -> UUID:
    try:
        return UUID(str(value))
    except (TypeError, ValueError) as exc:
        raise TenantAdministrationValidationError(f"invalid {label}") from exc


def _tenant(row: Any) -> AdminTenant:
    created_at = field_value(row, "created_at")
    updated_at = field_value(row, "updated_at")
    realm_id = field_value(row, "realm_id")
    return AdminTenant(
        tenant_id=str(field_value(row, "id")),
        realm_id=str(realm_id) if realm_id else None,
        slug=str(field_value(row, "slug")),
        name=str(field_value(row, "name")),
        email=str(field_value(row, "email")),
        is_active=bool(field_value(row, "is_active", True)),
        created_at=created_at.isoformat() if created_at else None,
        updated_at=updated_at.isoformat() if updated_at else None,
    )


async def require_tenant_administrator(
    request: object, db: object
) -> TenantAdministrator:
    actor = await resolve_admin_user_from_request(request, db=db)
    if actor is None:
        raise TenantAdministratorAuthenticationError(
            "authenticated admin session required"
        )
    return TenantAdministrator(
        actor_id=str(field_value(actor, "id")),
        tenant_id=str(field_value(actor, "tenant_id")),
        is_admin=bool(field_value(actor, "is_admin", False)),
        is_superuser=bool(field_value(actor, "is_superuser", False)),
    )


def build_tenant_administration_capability(
    db: object,
) -> TenantAdministrationCapability:
    async def lister() -> tuple[AdminTenant, ...]:
        return tuple(_tenant(row) for row in await list_table_records(Tenant, db))

    async def reader(tenant_id: str) -> AdminTenant | None:
        row = await read_table_record(Tenant, db, _uuid(tenant_id, label="tenant_id"))
        return _tenant(row) if row is not None else None

    async def creator(spec: AdminTenantCreate) -> AdminTenant:
        slug = spec.slug.strip().lower()
        name = spec.name.strip()
        email = spec.email.strip().lower()
        for filters in ({"slug": slug}, {"name": name}, {"email": email}):
            if await first_table_record(Tenant, db, filters) is not None:
                raise TenantAdministrationConflictError(
                    "tenant slug, name, or email already exists"
                )
        row = await create_table_record(
            Tenant,
            db,
            {
                "realm_id": (
                    _uuid(spec.realm_id, label="realm_id")
                    if spec.realm_id is not None
                    else None
                ),
                "slug": slug,
                "name": name,
                "email": email,
            },
        )
        return _tenant(row)

    async def updater(tenant_id: str, spec: AdminTenantUpdate) -> AdminTenant:
        key = _uuid(tenant_id, label="tenant_id")
        row = await read_table_record(Tenant, db, key)
        if row is None:
            raise TenantAdministrationNotFoundError("tenant not found")
        changes: dict[str, object] = {}
        if spec.realm_id is not None:
            changes["realm_id"] = _uuid(spec.realm_id, label="realm_id")
        if spec.slug is not None:
            changes["slug"] = spec.slug.strip().lower()
        if spec.name is not None:
            changes["name"] = spec.name.strip()
        if spec.email is not None:
            changes["email"] = spec.email.strip().lower()
        if spec.is_active is not None:
            changes["is_active"] = spec.is_active
        for field in ("slug", "name", "email"):
            value = changes.get(field)
            if value is None:
                continue
            duplicate = await first_table_record(Tenant, db, {field: value})
            if duplicate is not None and str(field_value(duplicate, "id")) != str(key):
                raise TenantAdministrationConflictError(
                    "tenant slug, name, or email already exists"
                )
        if changes:
            row = await update_table_record(Tenant, db, key, changes)
        return _tenant(row)

    async def deleter(tenant_id: str) -> AdminTenant:
        key = _uuid(tenant_id, label="tenant_id")
        row = await read_table_record(Tenant, db, key)
        if row is None:
            raise TenantAdministrationNotFoundError("tenant not found")
        snapshot = _tenant(row)
        await delete_table_record(Tenant, db, key)
        return snapshot

    return TenantAdministrationCapability(
        lister=lister,
        creator=creator,
        reader=reader,
        updater=updater,
        deleter=deleter,
    )


def tenant_administration_for_request(
    request: object,
    db: object,
) -> TenantAdministrationCapability:
    state = getattr(getattr(request, "app", None), "state", None)
    registry = getattr(state, "tigrbl_auth_capability_registry", None)
    if registry is not None:
        try:
            capability = registry.materialize("identity-admin.tenants", db)
        except KeyError:
            pass
        else:
            if not isinstance(capability, TenantAdministrationCapability):
                raise TypeError(
                    "tenant capability factory returned an invalid capability"
                )
            return capability
    return build_tenant_administration_capability(db)


__all__ = [
    "build_tenant_administration_capability",
    "get_db",
    "require_tenant_administrator",
    "tenant_administration_for_request",
]
