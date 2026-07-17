import pytest

from tigrbl_policy_administration_memory_provider import ABACAdministrator


@pytest.mark.asyncio
async def test_abac_administrator_supports_policies_and_attributes(administrator_storage):
    abac = ABACAdministrator(administrator_storage)
    policy = await abac.upsert_policy(
        "same-tenant-key-rotation",
        permission="key.rotate",
        required_attributes={"tenant_id": "tenant-a", "mfa": True},
    )

    reader = ABACAdministrator(administrator_storage)
    decision = await reader.decide(permission="key.rotate", attributes={"tenant_id": "tenant-a", "mfa": True})

    assert policy.required_attributes == {"tenant_id": "tenant-a", "mfa": True}
    assert decision.allowed
    assert decision.matched == ("same-tenant-key-rotation",)


@pytest.mark.asyncio
async def test_abac_administrator_surfaces_denials(administrator_storage):
    abac = ABACAdministrator(administrator_storage)
    await abac.upsert_policy(
        "same-tenant-key-rotation",
        permission="key.rotate",
        required_attributes={"tenant_id": "tenant-a", "mfa": True},
    )

    decision = await ABACAdministrator(administrator_storage).decide(permission="key.rotate", attributes={"tenant_id": "tenant-b", "mfa": True})

    assert not decision.allowed
    assert decision.reason == "permission denied by ABAC attributes"
