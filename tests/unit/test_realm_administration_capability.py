from __future__ import annotations

import asyncio
from pathlib import Path

import pytest

from tigrbl_identity_admin_control_plane import RealmAdministrationCapability
from tigrbl_identity_contracts.admin_realms import (
    AdminRealm,
    AdminRealmCreate,
    AdminRealmUpdate,
    RealmAdministrationValidationError,
)
from tigrbl_identity_contracts.admin_tenants import (
    AdminTenant,
    AdminTenantCreate,
    PlatformAdministrator,
    TenantAdministrationPolicyError,
)


ROOT = Path(__file__).resolve().parents[2]
REALM_API = (
    ROOT
    / "pkgs/90-backend-apps/tigrbl-auth-backend-app-platform-admin/src/tigrbl_auth_backend_app_platform_admin/realms.py"
)


def _realm(realm_id: str = "realm-1") -> AdminRealm:
    return AdminRealm(realm_id, "realm-one", "Realm One")


def _capability(
    events: list[str], *, tenants: tuple[AdminTenant, ...] = ()
) -> RealmAdministrationCapability:
    async def lister():
        events.append("list")
        return (_realm(),)

    async def creator(spec: AdminRealmCreate):
        events.append(f"create:{spec.slug}")
        return _realm()

    async def reader(realm_id: str):
        events.append(f"read:{realm_id}")
        return _realm(realm_id)

    async def updater(realm_id: str, spec: AdminRealmUpdate):
        events.append(f"update:{realm_id}:{spec.name}")
        return _realm(realm_id)

    async def deleter(realm_id: str):
        events.append(f"delete:{realm_id}")
        return _realm(realm_id)

    async def tenant_lister(actor: PlatformAdministrator, realm_id: str):
        events.append(f"list-tenants:{realm_id}")
        return tenants

    async def tenant_creator(actor: PlatformAdministrator, spec: AdminTenantCreate):
        events.append(f"create-tenant:{spec.realm_id}:{spec.slug}")
        return AdminTenant("tenant-1", spec.realm_id, spec.slug, spec.name, spec.email)

    return RealmAdministrationCapability(
        lister=lister,
        creator=creator,
        reader=reader,
        updater=updater,
        deleter=deleter,
        tenant_lister=tenant_lister,
        tenant_creator=tenant_creator,
    )


def test_realm_capability_reports_complete_operation_set() -> None:
    report = _capability([]).capability_report()

    assert report["capability_id"] == "identity-admin.realms"
    assert set(report["operations"]) == {
        "create_realm",
        "create_realm_tenant",
        "delete_realm",
        "list_realm_tenants",
        "list_realms",
        "read_realm",
        "update_realm",
    }
    assert set(report["delegated_operations"]) == set(report["operations"])


def test_realm_capability_requires_superuser_for_reads_and_mutations() -> None:
    admin = PlatformAdministrator("actor", "tenant-1", is_admin=True)
    capability = _capability([])

    with pytest.raises(TenantAdministrationPolicyError):
        asyncio.run(capability.call("list_realms", admin))
    with pytest.raises(TenantAdministrationPolicyError):
        asyncio.run(capability.call("delete_realm", admin, "realm-1"))


def test_realm_capability_prevents_delete_while_tenants_exist() -> None:
    actor = PlatformAdministrator("actor", "tenant-1", True, True)
    tenant = AdminTenant(
        "tenant-1", "realm-1", "tenant", "Tenant", "tenant@example.test"
    )
    events: list[str] = []
    capability = _capability(events, tenants=(tenant,))

    with pytest.raises(RealmAdministrationValidationError, match="still owns tenants"):
        asyncio.run(capability.call("delete_realm", actor, "realm-1"))
    assert not any(event.startswith("delete:") for event in events)


def test_realm_tenant_creation_binds_the_path_realm() -> None:
    actor = PlatformAdministrator("actor", "tenant-1", True, True)
    events: list[str] = []
    capability = _capability(events)
    spec = AdminTenantCreate("wrong-realm", "tenant", "Tenant", "tenant@example.test")

    result = asyncio.run(capability.call("create_realm_tenant", actor, "realm-1", spec))

    assert result.value.realm_id == "realm-1"
    assert "create-tenant:realm-1:tenant" in events


def test_realm_api_is_http_only_and_has_no_storage_runtime_imports() -> None:
    source = REALM_API.read_text(encoding="utf-8")

    assert "tigrbl_identity_storage" not in source
    assert "create_table_record" not in source
    assert "update_table_record" not in source
    assert "delete_table_record" not in source
    assert "realm_administration_for_request" in source
