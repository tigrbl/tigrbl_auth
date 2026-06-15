from __future__ import annotations

import tests.unit.formal_auth_helpers  # noqa: F401

from tigrbl_authz_policy import AuthorityScope, DelegationGrant, prove_delegation_attenuation


def test_delegation_attenuation_t2_rejects_broader_action_resource_tenant_and_realm() -> None:
    source = (AuthorityScope("tenant-a", "client.read", resource="app:1", realm="realm-a"),)

    proof = prove_delegation_attenuation(
        source_scopes=source,
        grant=DelegationGrant(
            delegator="subject:alice",
            delegate="subject:bob",
            tenant_ids=("tenant-a", "tenant-b"),
            actions=("client.read", "client.write"),
            resources=("app:1", "app:2"),
            realm="realm-b",
        ),
    )

    assert proof.passed is False
    assert {scope.tenant_id for scope in proof.uncovered_scopes} == {"tenant-a", "tenant-b"}
    assert {scope.realm for scope in proof.uncovered_scopes} == {"realm-b"}


def test_delegation_attenuation_t2_checks_chained_attenuation_and_wildcard_narrowing() -> None:
    first_hop = prove_delegation_attenuation(
        source_scopes=(AuthorityScope("tenant-a", "client.*"),),
        grant=DelegationGrant(
            delegator="subject:alice",
            delegate="subject:bob",
            tenant_ids=("tenant-a",),
            actions=("client.write",),
            provenance_id="prov:1",
        ),
        known_provenance_ids=("prov:1",),
    )
    second_hop = prove_delegation_attenuation(
        source_scopes=first_hop.delegated_scopes,
        grant=DelegationGrant(
            delegator="subject:bob",
            delegate="subject:carol",
            tenant_ids=("tenant-a",),
            actions=("client.delete",),
            provenance_id="prov:2",
        ),
        known_provenance_ids=("prov:2",),
    )

    assert first_hop.passed is True
    assert second_hop.passed is False
    assert tuple(scope.action for scope in second_hop.uncovered_scopes) == ("client.delete",)


def test_delegation_attenuation_t2_rejects_revoked_expired_missing_provenance_and_policy_version_conflicts() -> None:
    base = {
        "delegator": "subject:alice",
        "delegate": "subject:bob",
        "tenant_ids": ("tenant-a",),
        "actions": ("client.read",),
    }
    source = (AuthorityScope("tenant-a", "client.*"),)

    revoked = prove_delegation_attenuation(source_scopes=source, grant=DelegationGrant(**base, revoked=True))
    expired = prove_delegation_attenuation(
        source_scopes=source,
        grant=DelegationGrant(**base, expires_at="2026-06-07T00:00:00+00:00"),
        evaluated_at="2026-06-07T00:00:01+00:00",
    )
    missing_provenance = prove_delegation_attenuation(
        source_scopes=source,
        grant=DelegationGrant(**base),
        known_provenance_ids=("prov:known",),
    )
    bad_version = prove_delegation_attenuation(
        source_scopes=source,
        grant=DelegationGrant(**base, policy_version="policy:v2", provenance_id="prov:known"),
        known_provenance_ids=("prov:known",),
        allowed_policy_versions=("policy:v1",),
    )

    assert revoked.failures == ("delegation grant is revoked",)
    assert expired.failures == ("delegation grant is expired",)
    assert missing_provenance.failures == ("delegation provenance is required",)
    assert bad_version.failures == ("delegation policy version 'policy:v2' is not allowed",)
