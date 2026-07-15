from __future__ import annotations

import asyncio
from pathlib import Path

import pytest

from tigrbl_identity_admin_control_plane import TenantAdministrationCapability
from tigrbl_identity_contracts.admin_tenants import (
    AdminTenant,
    AdminTenantCreate,
    AdminTenantUpdate,
    TenantAdministrationPolicyError,
    TenantAdministrationValidationError,
    TenantAdministrator,
)


ROOT = Path(__file__).resolve().parents[2]
TENANT_API = (
    ROOT
    / "pkgs/80-apis/tigrbl-auth-api-platform-admin/src"
    / "tigrbl_auth_api_platform_admin/tenants.py"
)


def _tenant(tenant_id: str = "tenant-1", slug: str = "tenant-one") -> AdminTenant:
    return AdminTenant(
        tenant_id=tenant_id,
        realm_id=None,
        slug=slug,
        name="Tenant One",
        email="tenant@example.test",
    )


def _capability(events: list[str]) -> TenantAdministrationCapability:
    async def lister():
        events.append("list")
        return (_tenant(),)

    async def creator(spec: AdminTenantCreate):
        events.append(f"create:{spec.slug}")
        return _tenant()

    async def reader(tenant_id: str):
        events.append(f"read:{tenant_id}")
        return _tenant(tenant_id)

    async def updater(tenant_id: str, spec: AdminTenantUpdate):
        events.append(f"update:{tenant_id}:{spec.name}")
        return _tenant(tenant_id)

    async def deleter(tenant_id: str):
        events.append(f"delete:{tenant_id}")
        return _tenant(tenant_id)

    return TenantAdministrationCapability(
        lister=lister,
        creator=creator,
        reader=reader,
        updater=updater,
        deleter=deleter,
    )


def test_tenant_capability_reports_complete_delegated_operation_set() -> None:
    capability = _capability([])
    report = capability.capability_report()

    assert report["capability_id"] == "identity-admin.tenants"
    assert report["operations"] == (
        "list_tenants",
        "create_tenant",
        "read_tenant",
        "update_tenant",
        "delete_tenant",
    )
    assert set(report["delegated_operations"]) == set(report["operations"])


def test_tenant_capability_enforces_admin_and_superuser_policy() -> None:
    capability = _capability([])
    non_admin = TenantAdministrator("actor", "tenant-2")
    admin = TenantAdministrator("actor", "tenant-2", is_admin=True)

    with pytest.raises(TenantAdministrationPolicyError):
        asyncio.run(capability.call("list_tenants", non_admin))
    with pytest.raises(TenantAdministrationPolicyError):
        asyncio.run(
            capability.call(
                "create_tenant",
                admin,
                AdminTenantCreate(None, "new", "New", "new@example.test"),
            )
        )


def test_tenant_capability_prevents_default_and_current_tenant_deletion() -> None:
    superuser = TenantAdministrator(
        "actor",
        "tenant-1",
        is_admin=True,
        is_superuser=True,
    )

    public = _capability([])
    public._reader = lambda tenant_id: _tenant(tenant_id, "public")
    with pytest.raises(TenantAdministrationValidationError, match="default public"):
        asyncio.run(public.call("delete_tenant", superuser, "tenant-public"))

    current = _capability([])
    with pytest.raises(
        TenantAdministrationValidationError, match="current administrator"
    ):
        asyncio.run(current.call("delete_tenant", superuser, "tenant-1"))


def test_tenant_api_is_http_only_and_has_no_storage_runtime_imports() -> None:
    source = TENANT_API.read_text(encoding="utf-8")

    assert "tigrbl_identity_storage" not in source
    assert "create_table_record" not in source
    assert "update_table_record" not in source
    assert "delete_table_record" not in source
    assert "tenant_administration_for_request" in source
