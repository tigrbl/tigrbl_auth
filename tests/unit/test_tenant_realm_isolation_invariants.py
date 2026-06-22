from __future__ import annotations

import tests.unit.formal_auth_helpers  # noqa: F401

from tigrbl_authz_policy import validate_tenant_realm_isolation
from tigrbl_authz_policy_authority_derivation_graph import (
    AuthorityDerivationGraph,
    AuthorityEdge,
    AuthorityNode,
    AuthorityScope,
)


def test_tenant_realm_isolation_t1_detects_cross_tenant_and_cross_realm_paths() -> None:
    graph = AuthorityDerivationGraph(
        nodes=(
            AuthorityNode("subject:alice", "subject", tenant_id="tenant-a", realm="realm-a"),
            AuthorityNode("authority:a", "authority", tenant_id="tenant-a", realm="realm-a"),
            AuthorityNode("authority:b", "authority", tenant_id="tenant-b", realm="realm-b"),
        ),
        edges=(
            AuthorityEdge("edge:a", "subject:alice", "authority:a", "grant", (AuthorityScope("tenant-a", "client.read", realm="realm-a"),)),
            AuthorityEdge("edge:b", "subject:alice", "authority:b", "grant", (AuthorityScope("tenant-b", "client.read", realm="realm-b"),)),
        ),
    )

    report = validate_tenant_realm_isolation(
        graph=graph,
        subject="subject:alice",
        expected_tenant_id="tenant-a",
        expected_realm="realm-a",
    )

    assert report.passed is False
    assert "path edge:b crosses tenant 'tenant-b'" in report.failures
    assert "path edge:b crosses realm 'realm-b'" in report.failures
