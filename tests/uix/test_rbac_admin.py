import pytest

from tigrbl_policy_administration_memory_provider import RBACAdministrator


@pytest.mark.asyncio
async def test_rbac_administrator_supports_roles_permissions_and_assignments(administrator_storage):
    rbac = RBACAdministrator(administrator_storage)
    role = await rbac.upsert_role("support-admin", ("tenant.read", "client.disable"), tenant_id="tenant-a")
    await rbac.assign_role("alice", "support-admin", tenant_id="tenant-a")

    reader = RBACAdministrator(administrator_storage)
    decision = await reader.decide("alice", "client.disable", "tenant-a")

    assert role.permissions == ("client.disable", "tenant.read")
    assert await reader.assignments_for("alice", "tenant-a") == ("support-admin",)
    assert decision.allowed
    assert decision.matched == ("support-admin",)


@pytest.mark.asyncio
async def test_rbac_administrator_surfaces_denials(administrator_storage):
    rbac = RBACAdministrator(administrator_storage)
    await rbac.upsert_role("auditor", ("tenant.read",), tenant_id="tenant-a")
    await rbac.assign_role("bob", "auditor", tenant_id="tenant-a")

    decision = await RBACAdministrator(administrator_storage).decide("bob", "key.rotate", "tenant-a")

    assert not decision.allowed
    assert decision.reason == "permission denied by RBAC role assignments"
