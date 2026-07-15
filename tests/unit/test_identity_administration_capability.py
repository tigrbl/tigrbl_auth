from __future__ import annotations

import asyncio
from pathlib import Path

import pytest

from tigrbl_identity_admin_control_plane import IdentityAdministrationCapability
from tigrbl_identity_contracts.admin_identities import (
    AdminIdentity,
    AdminIdentityCreate,
    AdminIdentityUpdate,
    IdentityAdministrationPolicyError,
    IdentityAdministrationValidationError,
)
from tigrbl_identity_contracts.admin_tenants import PlatformAdministrator


ROOT = Path(__file__).resolve().parents[2]
IDENTITY_API = (
    ROOT
    / "pkgs/80-apis/tigrbl-auth-api-platform-admin/src/tigrbl_auth_api_platform_admin/identities.py"
)


def _identity(
    identity_id: str = "identity-1",
    tenant_id: str = "tenant-1",
    *,
    is_admin: bool = False,
    is_superuser: bool = False,
) -> AdminIdentity:
    return AdminIdentity(
        identity_id,
        tenant_id,
        "user-one",
        "user@example.test",
        is_admin=is_admin,
        is_superuser=is_superuser,
    )


def _capability(
    events: list[str],
    *,
    current: AdminIdentity | None = None,
) -> IdentityAdministrationCapability:
    async def lister(tenant_id: str):
        events.append(f"list:{tenant_id}")
        return (_identity(tenant_id=tenant_id),)

    async def creator(spec: AdminIdentityCreate):
        events.append(f"create:{spec.tenant_id}:{spec.username}")
        return _identity(tenant_id=spec.tenant_id)

    async def reader(identity_id: str):
        events.append(f"read:{identity_id}")
        return current or _identity(identity_id)

    async def updater(identity_id: str, spec: AdminIdentityUpdate):
        events.append(f"update:{identity_id}:{spec.username}")
        return current or _identity(identity_id)

    async def deleter(identity_id: str):
        events.append(f"delete:{identity_id}")
        return current or _identity(identity_id)

    return IdentityAdministrationCapability(
        lister=lister,
        creator=creator,
        reader=reader,
        updater=updater,
        deleter=deleter,
    )


def test_identity_capability_reports_complete_operation_set() -> None:
    report = _capability([]).capability_report()

    assert report["capability_id"] == "identity-admin.identities"
    assert set(report["operations"]) == {
        "create_identity",
        "delete_identity",
        "list_identities",
        "read_identity",
        "update_identity",
    }
    assert set(report["delegated_operations"]) == set(report["operations"])


def test_identity_capability_rejects_cross_tenant_non_superuser_access() -> None:
    actor = PlatformAdministrator("actor", "tenant-1", is_admin=True)

    with pytest.raises(IdentityAdministrationPolicyError, match="cross-tenant"):
        asyncio.run(_capability([]).call("list_identities", actor, "tenant-2"))


def test_identity_capability_rejects_privilege_escalation() -> None:
    actor = PlatformAdministrator("actor", "tenant-1", is_admin=True)
    spec = AdminIdentityCreate(
        "tenant-1",
        "new-admin",
        "admin@example.test",
        "password",
        is_admin=True,
    )

    with pytest.raises(IdentityAdministrationPolicyError, match="privileged"):
        asyncio.run(_capability([]).call("create_identity", actor, spec))


def test_identity_capability_prevents_self_deactivation_and_deletion() -> None:
    current = _identity("actor", "tenant-1", is_admin=True, is_superuser=True)
    actor = PlatformAdministrator("actor", "tenant-1", is_admin=True, is_superuser=True)
    capability = _capability([], current=current)

    with pytest.raises(IdentityAdministrationValidationError, match="deactivate"):
        asyncio.run(
            capability.call(
                "update_identity",
                actor,
                "actor",
                AdminIdentityUpdate(is_active=False),
            )
        )
    with pytest.raises(IdentityAdministrationValidationError, match="delete"):
        asyncio.run(capability.call("delete_identity", actor, "actor"))


def test_identity_api_is_http_only_and_does_not_hash_or_mutate_storage() -> None:
    source = IDENTITY_API.read_text(encoding="utf-8")

    assert "tigrbl_identity_storage" not in source
    assert "BcryptSecretHasher" not in source
    assert "create_table_record" not in source
    assert "update_table_record" not in source
    assert "delete_table_record" not in source
    assert "identity_administration_for_request" in source
