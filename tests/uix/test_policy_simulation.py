import pytest

from tigrbl_auth.uix import ABACAdministrator, RBACAdministrator, simulate_policy


@pytest.mark.asyncio
async def test_policy_simulation_returns_allow_deny_and_explanations(administrator_storage):
    rbac = RBACAdministrator(administrator_storage)
    await rbac.upsert_role("security-admin", ("key.rotate",), tenant_id="tenant-a")
    await rbac.assign_role("alice", "security-admin", tenant_id="tenant-a")

    abac = ABACAdministrator(administrator_storage)
    await abac.upsert_policy(
        "same-tenant-mfa",
        permission="key.rotate",
        required_attributes={"tenant_id": "tenant-a", "mfa": True},
    )

    allowed = await simulate_policy(
        rbac=rbac,
        abac=abac,
        subject="alice",
        permission="key.rotate",
        attributes={"tenant_id": "tenant-a", "mfa": True},
    )
    denied = await simulate_policy(
        rbac=rbac,
        abac=abac,
        subject="alice",
        permission="key.rotate",
        attributes={"tenant_id": "tenant-a", "mfa": False},
    )

    assert allowed.allowed
    assert allowed.matched == ("security-admin", "same-tenant-mfa")
    assert not denied.allowed
    assert "ABAC attributes" in denied.reason
