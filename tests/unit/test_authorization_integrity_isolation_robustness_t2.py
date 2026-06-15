from __future__ import annotations

import tests.unit.formal_auth_helpers  # noqa: F401

from tigrbl_authz_policy import (
    AuthorizationReference,
    AuthorityDerivationGraph,
    AuthorityEdge,
    AuthorityNode,
    AuthorityScope,
    ReferenceCatalog,
    TrustEdge,
    validate_authorization_referential_integrity,
    validate_tenant_realm_isolation,
    validate_trust_graph_integrity,
)


def test_authorization_integrity_t2_detects_orphans_dangling_provenance_policy_versions_and_duplicates_deterministically() -> None:
    catalog = ReferenceCatalog(
        subjects=("subject:alice",),
        tenants=("tenant-a",),
        realms=("realm-a",),
        policies=("policy:read",),
        delegations=("delegation:1",),
        trust_domains=("domain-a",),
        authority_nodes=("authority:client",),
        provenance_ids=("prov:known",),
        policy_versions=("policy:v1",),
    )
    references = (
        AuthorizationReference("ref:subject", "subject", "subject:missing"),
        AuthorizationReference("ref:tenant", "tenant", "tenant-b"),
        AuthorizationReference("ref:realm", "realm", "realm-b"),
        AuthorizationReference("ref:policy", "policy", "policy:missing"),
        AuthorizationReference("ref:delegation", "delegation", "delegation:missing"),
        AuthorizationReference("ref:trust", "trust_domain", "domain-b"),
        AuthorizationReference("ref:authority", "authority_node", "authority:missing"),
        AuthorizationReference("ref:provenance", "provenance", "prov:missing"),
        AuthorizationReference("ref:version", "policy_version", "policy:v0"),
        AuthorizationReference("ref:reuse", "subject", "subject:alice"),
        AuthorizationReference("ref:reuse", "tenant", "tenant-a"),
        AuthorizationReference("ref:target-a", "subject", "shared:id"),
        AuthorizationReference("ref:target-b", "tenant", "shared:id"),
    )

    report_a = validate_authorization_referential_integrity(catalog=catalog, references=references)
    report_b = validate_authorization_referential_integrity(catalog=catalog, references=tuple(reversed(references)))

    assert report_a.failures == report_b.failures
    assert "ref:provenance references unknown provenance 'prov:missing'" in report_a.failures
    assert "ref:version references unknown policy_version 'policy:v0'" in report_a.failures
    assert "reference id 'ref:reuse' is reused across incompatible types" in report_a.failures
    assert "target id 'shared:id' is referenced as incompatible types" in report_a.failures


def test_trust_graph_integrity_t2_rejects_revoked_unknown_cycle_cross_domain_and_tenant_mismatch_edges() -> None:
    catalog = ReferenceCatalog(
        subjects=("issuer:a", "subject:b"),
        tenants=("tenant-a", "tenant-b"),
        trust_domains=("domain-a", "domain-b"),
    )

    report = validate_trust_graph_integrity(
        catalog=catalog,
        edges=(
            TrustEdge("trust:revoked", "issuer:a", "subject:b", "tenant-a", "domain-a", revoked=True),
            TrustEdge("trust:cycle", "subject:b", "issuer:a", "tenant-a", "domain-a"),
            TrustEdge("trust:unknown", "issuer:a", "subject:missing", "tenant-a", "domain-a"),
            TrustEdge("trust:tenant", "issuer:a", "subject:b", "tenant-a", "domain-a", subject_tenant_id="tenant-b"),
            TrustEdge("trust:domain", "issuer:a", "subject:b", "tenant-a", "domain-a", subject_trust_domain="domain-b"),
        ),
    )

    assert report.passed is False
    assert "trust edge 'trust:revoked' is revoked and cannot be active" in report.failures
    assert "trust graph cycle detected at 'issuer:a'" in report.failures
    assert "trust edge 'trust:unknown' has unknown subject 'subject:missing'" in report.failures
    assert "trust edge 'trust:tenant' crosses tenant 'tenant-a'->'tenant-b'" in report.failures
    assert "trust edge 'trust:domain' crosses trust domain 'domain-a'->'domain-b'" in report.failures


def test_tenant_realm_isolation_t2_detects_shared_role_surface_and_mixed_realm_paths_with_exact_edges() -> None:
    graph = AuthorityDerivationGraph(
        nodes=(
            AuthorityNode("subject:alice", "subject", tenant_id="tenant-a", realm="realm-a"),
            AuthorityNode("role:shared", "role", tenant_id="tenant-a", realm="realm-a"),
            AuthorityNode("surface:public", "surface", tenant_id="tenant-b", realm="realm-a"),
            AuthorityNode("surface:admin", "surface", tenant_id="tenant-a", realm="realm-b"),
            AuthorityNode("surface:verifier", "surface", tenant_id="tenant-a", realm="realm-a"),
        ),
        edges=(
            AuthorityEdge("edge:role-public", "subject:alice", "role:shared", "assignment", (AuthorityScope("tenant-b", "*", realm="realm-a"),)),
            AuthorityEdge("edge:role-admin", "subject:alice", "role:shared", "assignment", (AuthorityScope("tenant-a", "*", realm="realm-b"),)),
            AuthorityEdge("edge:role-verifier", "subject:alice", "role:shared", "assignment", (AuthorityScope("tenant-a", "*", realm="realm-a"),)),
            AuthorityEdge("edge:public", "role:shared", "surface:public", "surface", (AuthorityScope("tenant-b", "public.read", realm="realm-a"),)),
            AuthorityEdge("edge:admin", "role:shared", "surface:admin", "surface", (AuthorityScope("tenant-a", "admin.read", realm="realm-b"),)),
            AuthorityEdge("edge:verifier", "role:shared", "surface:verifier", "surface", (AuthorityScope("tenant-a", "verifier.read", realm="realm-a"),)),
        ),
    )

    report = validate_tenant_realm_isolation(
        graph=graph,
        subject="subject:alice",
        expected_tenant_id="tenant-a",
        expected_realm="realm-a",
    )

    assert "path edge:role-public/edge:public crosses tenant 'tenant-b'" in report.failures
    assert "path edge:role-admin/edge:admin crosses realm 'realm-b'" in report.failures
    assert all("edge:verifier" not in failure for failure in report.failures)


def test_trust_path_after_revocation_is_not_reachable_in_authority_graph() -> None:
    graph = AuthorityDerivationGraph(
        nodes=(AuthorityNode("issuer:a", "subject"), AuthorityNode("subject:b", "subject")),
        edges=(
            AuthorityEdge("edge:revoked-trust", "issuer:a", "subject:b", "trust", (AuthorityScope("tenant-a", "trust.impersonate"),), active=False),
        ),
    )

    proof = graph.prove_reachability("issuer:a", AuthorityScope("tenant-a", "trust.impersonate"))

    assert proof.reachable is False
