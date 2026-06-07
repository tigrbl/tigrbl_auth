from __future__ import annotations

import tests.unit.formal_auth_helpers  # noqa: F401

from tigrbl_auth.services.formal_authorization import DelegationGrant as FacadeDelegationGrant
from tigrbl_identity_policy import AuthorityScope, DelegationGrant, prove_delegation_attenuation


def test_delegation_attenuation_t0_exports_facade_identity() -> None:
    assert FacadeDelegationGrant is DelegationGrant


def test_delegation_attenuation_t1_accepts_bounded_delegation() -> None:
    grant = DelegationGrant(
        delegator="subject:alice",
        delegate="subject:bob",
        tenant_ids=("tenant-a",),
        actions=("client.read",),
        provenance_id="prov:delegation",
    )

    proof = prove_delegation_attenuation(
        source_scopes=(AuthorityScope("tenant-a", "client.*"),),
        grant=grant,
    )

    assert proof.passed is True
    assert proof.provenance_id == "prov:delegation"
    assert tuple(scope.action for scope in proof.delegated_scopes) == ("client.read",)


def test_delegation_attenuation_t1_rejects_uncovered_scope() -> None:
    proof = prove_delegation_attenuation(
        source_scopes=(AuthorityScope("tenant-a", "client.read"),),
        grant=DelegationGrant(
            delegator="subject:alice",
            delegate="subject:bob",
            tenant_ids=("tenant-a",),
            actions=("client.delete",),
        ),
    )

    assert proof.passed is False
    assert tuple(scope.action for scope in proof.uncovered_scopes) == ("client.delete",)
