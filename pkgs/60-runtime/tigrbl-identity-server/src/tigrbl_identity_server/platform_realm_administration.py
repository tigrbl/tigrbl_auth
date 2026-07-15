"""Durable runtime composition for realm-administration capability calls."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from tigrbl_identity_admin_control_plane import RealmAdministrationCapability
from tigrbl_identity_contracts.admin_realms import (
    AdminRealm,
    AdminRealmCreate,
    AdminRealmUpdate,
    RealmAdministrationConflictError,
    RealmAdministrationNotFoundError,
    RealmAdministrationValidationError,
)
from tigrbl_identity_contracts.admin_tenants import (
    AdminTenant,
    AdminTenantCreate,
    PlatformAdministrator,
)
from tigrbl_identity_storage.tables import Realm
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

from .platform_tenant_administration import (
    build_tenant_administration_capability,
    require_tenant_administrator,
)


def _uuid(value: str, *, label: str) -> UUID:
    try:
        return UUID(str(value))
    except (TypeError, ValueError) as exc:
        raise RealmAdministrationValidationError(f"invalid {label}") from exc


def _issuer_path(value: str | None, slug: str) -> str:
    text = (value if value is not None else f"/realms/{slug}").strip()
    if not text:
        return ""
    if not text.startswith("/"):
        text = f"/{text}"
    return text.rstrip("/")


def _realm(row: Any) -> AdminRealm:
    created_at = field_value(row, "created_at")
    updated_at = field_value(row, "updated_at")
    return AdminRealm(
        realm_id=str(field_value(row, "id")),
        slug=str(field_value(row, "slug")),
        name=str(field_value(row, "name")),
        issuer_path=str(field_value(row, "issuer_path", "")),
        description=field_value(row, "description"),
        created_at=created_at.isoformat() if created_at else None,
        updated_at=updated_at.isoformat() if updated_at else None,
    )


def build_realm_administration_capability(db: object) -> RealmAdministrationCapability:
    tenant_capability = build_tenant_administration_capability(db)

    async def lister() -> tuple[AdminRealm, ...]:
        return tuple(_realm(row) for row in await list_table_records(Realm, db))

    async def reader(realm_id: str) -> AdminRealm | None:
        row = await read_table_record(Realm, db, _uuid(realm_id, label="realm_id"))
        return _realm(row) if row is not None else None

    async def creator(spec: AdminRealmCreate) -> AdminRealm:
        slug = spec.slug.strip().lower()
        name = spec.name.strip()
        issuer_path = _issuer_path(spec.issuer_path, slug)
        for filters in (
            {"slug": slug},
            {"name": name},
            {"issuer_path": issuer_path},
        ):
            if await first_table_record(Realm, db, filters) is not None:
                raise RealmAdministrationConflictError(
                    "realm slug, name, or issuer path already exists"
                )
        row = await create_table_record(
            Realm,
            db,
            {
                "slug": slug,
                "name": name,
                "issuer_path": issuer_path,
                "description": spec.description,
            },
        )
        return _realm(row)

    async def updater(realm_id: str, spec: AdminRealmUpdate) -> AdminRealm:
        key = _uuid(realm_id, label="realm_id")
        row = await read_table_record(Realm, db, key)
        if row is None:
            raise RealmAdministrationNotFoundError("realm not found")
        changes: dict[str, object] = {}
        next_slug = str(field_value(row, "slug"))
        if spec.slug is not None:
            next_slug = spec.slug.strip().lower()
            changes["slug"] = next_slug
        if spec.name is not None:
            changes["name"] = spec.name.strip()
        if spec.issuer_path is not None:
            changes["issuer_path"] = _issuer_path(spec.issuer_path, next_slug)
        if spec.description is not None:
            changes["description"] = spec.description
        if changes:
            row = await update_table_record(Realm, db, key, changes)
        return _realm(row)

    async def deleter(realm_id: str) -> AdminRealm:
        key = _uuid(realm_id, label="realm_id")
        row = await read_table_record(Realm, db, key)
        if row is None:
            raise RealmAdministrationNotFoundError("realm not found")
        snapshot = _realm(row)
        await delete_table_record(Realm, db, key)
        return snapshot

    async def tenant_lister(
        actor: PlatformAdministrator,
        realm_id: str,
    ) -> tuple[AdminTenant, ...]:
        result = await tenant_capability.call("list_tenants", actor)
        return tuple(
            tenant for tenant in result.value if tenant.realm_id == str(realm_id)
        )

    async def tenant_creator(
        actor: PlatformAdministrator,
        spec: AdminTenantCreate,
    ) -> AdminTenant:
        result = await tenant_capability.call("create_tenant", actor, spec)
        return result.value

    return RealmAdministrationCapability(
        lister=lister,
        creator=creator,
        reader=reader,
        updater=updater,
        deleter=deleter,
        tenant_lister=tenant_lister,
        tenant_creator=tenant_creator,
    )


async def require_realm_administrator(
    request: object,
    db: object,
) -> PlatformAdministrator:
    return await require_tenant_administrator(request, db)


def realm_administration_for_request(
    request: object,
    db: object,
) -> RealmAdministrationCapability:
    state = getattr(getattr(request, "app", None), "state", None)
    registry = getattr(state, "tigrbl_auth_capability_registry", None)
    if registry is not None:
        try:
            capability = registry.materialize("identity-admin.realms", db)
        except KeyError:
            pass
        else:
            if not isinstance(capability, RealmAdministrationCapability):
                raise TypeError(
                    "realm capability factory returned an invalid capability"
                )
            return capability
    return build_realm_administration_capability(db)


__all__ = [
    "build_realm_administration_capability",
    "get_db",
    "realm_administration_for_request",
    "require_realm_administrator",
]
