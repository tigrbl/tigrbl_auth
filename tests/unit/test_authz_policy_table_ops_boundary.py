from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest
from tigrbl_identity_storage_runtime import (
    assign_role,
    list_active_attribute_policies,
    first_table_record,
    grant_delegated_scope,
    grant_membership,
    list_table_records,
    revoke_delegated_scope,
    role_names_for_principal,
    upsert_attribute_policy,
)


ROOT = Path(__file__).resolve().parents[2]


async def _op(model, operation: str, db, **payload):
    return await getattr(model, operation)({"payload": payload, "db": db})


async def _runtime_op(operation, db, **payload):
    return await operation({"payload": payload, "db": db})


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
async def test_rbac_assignment_helpers_are_runtime_owned(administrator_storage) -> None:
    await _runtime_op(grant_membership,
        administrator_storage,
        tenant_id="tenant-a",
        principal_id="alice",
        roles=("reader",),
    )
    await _runtime_op(assign_role,
        administrator_storage,
        tenant_id="tenant-a",
        principal_id="alice",
        role_name="editor",
    )
    await _runtime_op(grant_membership,
        administrator_storage,
        tenant_id="tenant-b",
        principal_id="alice",
        roles=("other-tenant",),
    )
    await _runtime_op(grant_membership,
        administrator_storage,
        tenant_id="tenant-a",
        principal_id="bob",
        roles=("revoked",),
        status="revoked",
    )

    assert await _runtime_op(role_names_for_principal,
        administrator_storage,
        principal_id="alice",
        tenant_id="tenant-a",
    ) == ("editor", "reader")
    assert await _runtime_op(role_names_for_principal,
        administrator_storage,
        principal_id="alice",
    ) == ("editor", "other-tenant", "reader")
    assert await _runtime_op(role_names_for_principal,
        administrator_storage,
        principal_id="bob",
        tenant_id="tenant-a",
    ) == ()


@pytest.mark.asyncio
async def test_abac_policy_condition_helpers_are_runtime_owned(administrator_storage) -> None:
    row, conditions = await _runtime_op(upsert_attribute_policy,
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

    row, conditions = await _runtime_op(upsert_attribute_policy,
        administrator_storage,
        name="tenant-risk",
        tenant_id="tenant-a",
        permission="client.update",
        required_attributes={"tenant_id": "tenant-a", "mfa": True},
        dynamic_conditions=(
            {"field_name": "device_trust", "operator": "eq", "expected": "managed"},
        ),
    )

    active = await _runtime_op(list_active_attribute_policies,
        administrator_storage,
        tenant_id="tenant-a",
    )

    assert row["required_attributes"] == {"tenant_id": "tenant-a", "mfa": True}
    assert len(active) == 1
    active_row, active_conditions = active[0]
    assert active_row["name"] == "tenant-risk"
    assert [condition["field_name"] for condition in active_conditions] == ["device_trust"]


@pytest.mark.asyncio
async def test_delegated_admin_scope_ops_are_runtime_owned(administrator_storage) -> None:
    from tigrbl_identity_storage.tables.delegated_admin_scope import DelegatedAdminScope

    granted = await _runtime_op(grant_delegated_scope,
        administrator_storage,
        subject="delegate",
        tenant_ids=["tenant-a"],
        permissions=["client.read"],
        visible_client_fields=["id", "name"],
        mutable_client_fields=["name"],
    )
    looked_up = await first_table_record(DelegatedAdminScope, administrator_storage, {"subject": "delegate"})

    assert looked_up == granted
    assert [
        row["subject"]
        for row in await list_table_records(DelegatedAdminScope, administrator_storage, {"status": "active"})
    ] == ["delegate"]

    revoked = await _runtime_op(revoke_delegated_scope, administrator_storage, subject="delegate")

    assert revoked["status"] == "revoked"
    assert await list_table_records(DelegatedAdminScope, administrator_storage, {"status": "active"}) == []
