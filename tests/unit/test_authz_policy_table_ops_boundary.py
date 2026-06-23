from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]


def test_authz_policy_store_facade_is_removed() -> None:
    assert importlib.util.find_spec("tigrbl_identity_storage.authz_policy_store") is None
    assert not (
        ROOT
        / "pkgs"
        / "01-storage"
        / "tigrbl-identity-storage"
        / "src"
        / "tigrbl_identity_storage"
        / "authz_policy_store.py"
    ).exists()


@pytest.mark.asyncio
async def test_rbac_assignment_helpers_are_table_owned(administrator_storage) -> None:
    from tigrbl_identity_storage.tables.tenant_membership import TenantMembership

    await TenantMembership.grant_membership(
        administrator_storage,
        tenant_id="tenant-a",
        principal_id="alice",
        roles=("reader",),
    )
    await TenantMembership.assign_role(
        administrator_storage,
        tenant_id="tenant-a",
        principal_id="alice",
        role_name="editor",
    )
    await TenantMembership.grant_membership(
        administrator_storage,
        tenant_id="tenant-b",
        principal_id="alice",
        roles=("other-tenant",),
    )
    await TenantMembership.grant_membership(
        administrator_storage,
        tenant_id="tenant-a",
        principal_id="bob",
        roles=("revoked",),
        status="revoked",
    )

    assert await TenantMembership.role_names_for_principal(
        administrator_storage,
        principal_id="alice",
        tenant_id="tenant-a",
    ) == ("editor", "reader")
    assert await TenantMembership.role_names_for_principal(
        administrator_storage,
        principal_id="alice",
    ) == ("editor", "other-tenant", "reader")
    assert await TenantMembership.role_names_for_principal(
        administrator_storage,
        principal_id="bob",
        tenant_id="tenant-a",
    ) == ()


@pytest.mark.asyncio
async def test_abac_policy_condition_helpers_are_table_owned(administrator_storage) -> None:
    from tigrbl_identity_storage.tables.attribute_policy import AttributePolicy

    row, conditions = await AttributePolicy.upsert_with_conditions(
        administrator_storage,
        name="tenant-risk",
        tenant_id="tenant-a",
        permission="client.update",
        required_attributes={"tenant_id": "tenant-a"},
        dynamic_conditions=(
            {"field_name": "risk", "operator": "lte", "expected": 2},
        ),
    )
    assert row["name"] == "tenant-risk"
    assert [condition["field_name"] for condition in conditions] == ["risk"]

    row, conditions = await AttributePolicy.upsert_with_conditions(
        administrator_storage,
        name="tenant-risk",
        tenant_id="tenant-a",
        permission="client.update",
        required_attributes={"tenant_id": "tenant-a", "mfa": True},
        dynamic_conditions=(
            {"field_name": "device_trust", "operator": "eq", "expected": "managed"},
        ),
    )

    active = await AttributePolicy.list_active_with_conditions(
        administrator_storage,
        tenant_id="tenant-a",
    )

    assert row["required_attributes"] == {"tenant_id": "tenant-a", "mfa": True}
    assert len(active) == 1
    active_row, active_conditions = active[0]
    assert active_row["name"] == "tenant-risk"
    assert [condition["field_name"] for condition in active_conditions] == ["device_trust"]


@pytest.mark.asyncio
async def test_delegated_admin_scope_ops_remain_table_owned(administrator_storage) -> None:
    from tigrbl_identity_storage.tables.delegated_admin_scope import DelegatedAdminScope

    granted = await DelegatedAdminScope.grant_scope(
        administrator_storage,
        subject="delegate",
        tenant_ids=["tenant-a"],
        permissions=["client.read"],
        visible_client_fields=["id", "name"],
        mutable_client_fields=["name"],
    )
    looked_up = await DelegatedAdminScope.lookup(administrator_storage, subject="delegate")

    assert looked_up == granted
    assert [row["subject"] for row in await DelegatedAdminScope.list_active(administrator_storage)] == ["delegate"]

    revoked = await DelegatedAdminScope.revoke_scope(administrator_storage, subject="delegate")

    assert revoked["status"] == "revoked"
    assert await DelegatedAdminScope.list_active(administrator_storage) == []
