from __future__ import annotations

import uuid

import pytest

from tigrbl_identity_storage.tables import (
    DelegationGrant,
    DelegationGrantEdge,
    DelegationGrantProof,
    DelegationGrantTokenLink,
)
from tigrbl_identity_storage_runtime import (
    DelegationGrantEdgeRuntimeSpec,
    DelegationGrantProofRuntimeSpec,
    DelegationGrantRuntimeSpec,
    DelegationGrantTokenLinkRuntimeSpec,
    create_grant,
    initializeIdentityRuntimeTables,
    link_delegation_token,
    link_grant_edge,
    list_tokens_for_grant,
    persist_delegation_provenance,
    replace_grant,
    revoke_grant,
)


RUNTIME_SPECS = (
    DelegationGrantRuntimeSpec,
    DelegationGrantEdgeRuntimeSpec,
    DelegationGrantProofRuntimeSpec,
    DelegationGrantTokenLinkRuntimeSpec,
)
RUNTIME_MODELS = (
    DelegationGrant,
    DelegationGrantEdge,
    DelegationGrantProof,
    DelegationGrantTokenLink,
)


def _activate(monkeypatch, storage) -> None:
    initializeIdentityRuntimeTables(RUNTIME_SPECS)
    for model in RUNTIME_MODELS:
        runtime_handlers = model.handlers
        handlers = storage.handlers_for(model)
        for name, value in vars(runtime_handlers).items():
            if not hasattr(handlers, name):
                setattr(handlers, name, value)
        monkeypatch.setattr(model, "handlers", handlers, raising=False)


async def _grant(storage, **overrides):
    payload = {
        "delegator_subject": "principal:alice",
        "delegate_subject": "principal:bob",
        **overrides,
    }
    return await create_grant({"payload": payload, "db": storage})


@pytest.mark.asyncio
async def test_recursive_revocation_collapses_nonterminal_descendants(
    monkeypatch,
    administrator_storage,
) -> None:
    _activate(monkeypatch, administrator_storage)
    parent = await _grant(administrator_storage)
    child = await _grant(
        administrator_storage,
        parent_grant_id=parent["id"],
        delegator_subject="principal:bob",
        delegate_subject="principal:carol",
    )
    await link_grant_edge(
        {
            "payload": {
                "parent_grant_id": parent["id"],
                "child_grant_id": child["id"],
                "delegator_subject": "principal:bob",
                "delegate_subject": "principal:carol",
            },
            "db": administrator_storage,
        }
    )

    revoked = await revoke_grant(
        {
            "payload": {
                "grant_id": parent["id"],
                "revoked_by": "principal:admin",
                "reason": "policy-change",
                "collapse_descendants": True,
            },
            "db": administrator_storage,
        }
    )

    assert revoked["status"] == "revoked"
    grants = administrator_storage._bucket(DelegationGrant)
    child_record = next(row for row in grants if row["id"] == child["id"])
    assert child_record["status"] == "revoked"
    assert child_record["revoked_reason"] == "ancestor-revoked"
    assert administrator_storage._bucket(DelegationGrantEdge)[0]["active"] is False


@pytest.mark.asyncio
async def test_replacement_preserves_lineage_and_closes_prior_grant(
    monkeypatch,
    administrator_storage,
) -> None:
    _activate(monkeypatch, administrator_storage)
    current = await _grant(administrator_storage, policy_version="v1")

    replacement = await replace_grant(
        {
            "payload": {
                "grant_id": current["id"],
                "policy_version": "v2",
            },
            "db": administrator_storage,
        }
    )

    assert replacement["parent_grant_id"] == current["id"]
    assert replacement["policy_version"] == "v2"
    prior = next(
        row
        for row in administrator_storage._bucket(DelegationGrant)
        if row["id"] == current["id"]
    )
    assert prior["status"] == "replaced"
    assert prior["replaced_by_grant_id"] == replacement["id"]


@pytest.mark.asyncio
async def test_provenance_and_token_links_are_runtime_owned(
    monkeypatch,
    administrator_storage,
) -> None:
    _activate(monkeypatch, administrator_storage)
    grant = await _grant(administrator_storage)
    proof_hash = uuid.uuid4().hex
    proof = await persist_delegation_provenance(
        {
            "payload": {
                "grant_id": grant["id"],
                "source_scope_hash": "source",
                "delegated_scope_hash": "delegated",
                "attenuation_result": True,
                "proof_hash": proof_hash,
            },
            "db": administrator_storage,
        }
    )
    link = await link_delegation_token(
        {
            "payload": {
                "grant_id": grant["id"],
                "token_hash": "token-digest",
                "subject": "principal:bob",
            },
            "db": administrator_storage,
        }
    )

    assert proof["proof_hash"] == proof_hash
    assert link["grant_id"] == grant["id"]
    assert await list_tokens_for_grant(
        {
            "payload": {"grant_id": grant["id"]},
            "db": administrator_storage,
        }
    ) == [link]


def test_delegation_runtime_specs_preserve_operation_identity() -> None:
    aliases = {
        spec.model.__name__: {
            operation.alias
            for operation in spec.ops
            if operation.extra.get("owner_layer") == "30-storage-runtime"
        }
        for spec in RUNTIME_SPECS
    }
    assert aliases == {
        "DelegationGrant": {
            "create_grant",
            "inspect_grant",
            "list_grants",
            "activate_grant",
            "expire_grant",
            "replace_grant",
            "revoke_grant",
        },
        "DelegationGrantEdge": {"link_edge", "deactivate_children"},
        "DelegationGrantProof": {"persist_provenance"},
        "DelegationGrantTokenLink": {"link_token", "list_for_grant"},
    }


def test_layer01_delegation_models_have_no_lifecycle_methods() -> None:
    for name in (
        "create_grant",
        "inspect_grant",
        "list_grants",
        "activate_grant",
        "expire_grant",
        "replace_grant",
        "revoke_grant",
    ):
        assert not hasattr(DelegationGrant, name)
    assert not hasattr(DelegationGrantEdge, "link_edge")
    assert not hasattr(DelegationGrantProof, "persist_provenance")
    assert not hasattr(DelegationGrantTokenLink, "link_token")
