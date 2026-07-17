from __future__ import annotations

import asyncio
from pathlib import Path

import pytest

from tigrbl_identity_cli.operator_administration import (
    build_operator_administration_capability,
)
from tigrbl_identity_storage_runtime._resource_service.token_key_artifacts import (
    build_operator_jwks_payload,
)
from tigrbl_identity_storage_runtime.operator_store import OperationContext
from tigrbl_identity_storage_runtime.resource_service import OperatorStateError


TENANT_A = "tenant-a"
TENANT_B = "tenant-b"


def _context(tmp_path: Path, tenant: str, command: str) -> OperationContext:
    return OperationContext(
        repo_root=tmp_path,
        command=command,
        resource="keys",
        actor="test-operator",
        profile="production",
        tenant=tenant,
    )


async def _invoke(
    operation: str,
    context: OperationContext,
    **kwargs: object,
) -> object:
    capability = build_operator_administration_capability()
    return (await capability.call(operation, context, **kwargs)).value


def _record(result: object) -> dict[str, object]:
    record = getattr(result, "record", None)
    assert isinstance(record, dict)
    return record


@pytest.mark.asyncio
async def test_tenant_jwks_key_administration_operations_are_bound() -> None:
    capability = build_operator_administration_capability()

    report = capability.capability_report()
    assert {
        "key_create",
        "key_delete",
        "key_list",
        "key_seed",
        "key_update",
    } <= set(report["bound_operations"])


@pytest.mark.asyncio
async def test_tenant_jwks_key_seed_is_idempotent_and_publishable(
    tmp_path: Path,
) -> None:
    context = _context(tmp_path, TENANT_A, "tenant.keys.seed")

    first = await _invoke("key_seed", context)
    second = await _invoke("key_seed", context)

    assert getattr(first, "status") == "created"
    assert getattr(second, "status") == "skipped"
    assert _record(first)["id"] == f"{TENANT_A}-jwks-active"
    assert await asyncio.to_thread(
        build_operator_jwks_payload, tmp_path, tenant=TENANT_A
    ) == {
        "keys": [
            {
                "kid": f"{TENANT_A}-jwks-active",
                "alg": "EdDSA",
                "use": "sig",
                "kty": "OKP",
                "crv": "Ed25519",
                "status": "active",
            }
        ]
    }


@pytest.mark.asyncio
async def test_tenant_jwks_key_crud_is_tenant_scoped(tmp_path: Path) -> None:
    created_a = await _invoke(
        "key_create",
        _context(tmp_path, TENANT_A, "tenant.keys.create"),
        patch={
            "kid": "kid-a-active",
            "status": "active",
            "x": "pub-a",
            "publish": True,
        },
    )
    await _invoke(
        "key_create",
        _context(tmp_path, TENANT_B, "tenant.keys.create"),
        patch={
            "kid": "kid-b-active",
            "status": "active",
            "x": "pub-b",
            "publish": True,
        },
    )

    assert _record(created_a)["tenant"] == TENANT_A
    tenant_a_jwks = await asyncio.to_thread(
        build_operator_jwks_payload, tmp_path, tenant=TENANT_A
    )
    assert [item["kid"] for item in tenant_a_jwks["keys"]] == ["kid-a-active"]
    assert "pub-b" not in str(tenant_a_jwks)

    updated = await _invoke(
        "key_update",
        _context(tmp_path, TENANT_A, "tenant.keys.update"),
        record_id="kid-a-active",
        patch={"status": "retired", "publish": False},
    )
    assert _record(updated)["status"] == "retired"
    assert (
        await asyncio.to_thread(
            build_operator_jwks_payload, tmp_path, tenant=TENANT_A
        )
    )["keys"] == []

    listed = await _invoke(
        "key_list",
        _context(tmp_path, TENANT_A, "tenant.keys.list"),
    )
    assert [item["id"] for item in getattr(listed, "items")] == ["kid-a-active"]

    deleted = await _invoke(
        "key_delete",
        _context(tmp_path, TENANT_A, "tenant.keys.delete"),
        record_id="kid-a-active",
    )
    assert getattr(deleted, "status") == "deleted"

    empty = await _invoke(
        "key_list",
        _context(tmp_path, TENANT_A, "tenant.keys.list"),
    )
    assert getattr(empty, "items") == []


@pytest.mark.asyncio
async def test_tenant_jwks_key_mutations_reject_cross_tenant_updates(
    tmp_path: Path,
) -> None:
    await _invoke(
        "key_create",
        _context(tmp_path, TENANT_A, "tenant.keys.create"),
        patch={"kid": "kid-a", "x": "pub-a"},
    )

    with pytest.raises(OperatorStateError, match="was not found"):
        await _invoke(
            "key_update",
            _context(tmp_path, TENANT_B, "tenant.keys.update"),
            record_id="kid-a",
            patch={"status": "retired"},
        )
