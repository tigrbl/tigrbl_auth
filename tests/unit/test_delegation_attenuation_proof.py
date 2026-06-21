from __future__ import annotations

import tests.unit.formal_auth_helpers  # noqa: F401

from tigrbl_auth.services.formal_authorization import DelegationGrantSpec as FacadeDelegationGrantSpec
from tigrbl_authz_policy import AuthorityScope, DelegationGrantSpec, prove_delegation_attenuation


def test_delegation_attenuation_t0_exports_facade_identity() -> None:
    assert FacadeDelegationGrantSpec is DelegationGrantSpec


def test_delegation_attenuation_t1_accepts_bounded_delegation() -> None:
    grant = DelegationGrantSpec(
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
        grant=DelegationGrantSpec(
            delegator="subject:alice",
            delegate="subject:bob",
            tenant_ids=("tenant-a",),
            actions=("client.delete",),
        ),
    )

    assert proof.passed is False
    assert tuple(scope.action for scope in proof.uncovered_scopes) == ("client.delete",)
