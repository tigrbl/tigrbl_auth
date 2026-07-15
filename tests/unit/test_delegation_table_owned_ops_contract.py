from __future__ import annotations

from tigrbl_identity_storage_runtime import (
    DelegationGrantEdgeRuntimeSpec,
    DelegationGrantProofRuntimeSpec,
    DelegationGrantRuntimeSpec,
    DelegationGrantTokenLinkRuntimeSpec,
)


def _bound_ops(spec) -> set[str]:
    return {operation.alias for operation in spec.ops}


def test_delegation_runtime_specs_own_grant_and_provenance_ops() -> None:
    assert {
        "activate_grant",
        "create_grant",
        "expire_grant",
        "inspect_grant",
        "list_grants",
        "replace_grant",
        "revoke_grant",
    } <= _bound_ops(DelegationGrantRuntimeSpec)
    assert {"link_edge", "deactivate_children"} <= _bound_ops(
        DelegationGrantEdgeRuntimeSpec
    )
    assert {"persist_provenance"} <= _bound_ops(DelegationGrantProofRuntimeSpec)
    assert {"link_token", "list_for_grant"} <= _bound_ops(
        DelegationGrantTokenLinkRuntimeSpec
    )
