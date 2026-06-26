from __future__ import annotations

import tests.unit.formal_auth_helpers  # noqa: F401

from tigrbl_authz_policy_rules_concrete import (
    AuthorityDerivationGraph,
    AuthorityEdge,
    AuthorityNode,
    AuthorityScope,
    compute_authority_closure,
    validate_authority_graph_integrity,
)


def _nodes() -> tuple[AuthorityNode, ...]:
    return (
        AuthorityNode("subject:alice", "subject", tenant_id="tenant-a"),
        AuthorityNode("role:admin", "role", tenant_id="tenant-a"),
        AuthorityNode("group:ops", "group", tenant_id="tenant-a"),
        AuthorityNode("authority:client", "authority", tenant_id="tenant-a"),
    )


def test_authority_graph_robustness_t2_cycles_terminate_and_inactive_edges_are_excluded() -> None:
    graph = AuthorityDerivationGraph(
        nodes=_nodes(),
        edges=(
            AuthorityEdge("edge:subject-role", "subject:alice", "role:admin", "assignment", (AuthorityScope("tenant-a", "*"),)),
            AuthorityEdge("edge:role-group", "role:admin", "group:ops", "membership", (AuthorityScope("tenant-a", "*"),)),
            AuthorityEdge("edge:group-subject", "group:ops", "subject:alice", "cycle", (AuthorityScope("tenant-a", "*"),)),
            AuthorityEdge("edge:inactive", "role:admin", "authority:client", "grant", (AuthorityScope("tenant-a", "client.delete"),), active=False),
        ),
    )

    paths = graph.derive_paths("subject:alice")

    assert len(paths) == 3
    assert all("edge:inactive" not in path.edge_ids for path in paths)
    assert "authority:client" not in {path.target for path in paths}


def test_authority_graph_robustness_t2_detects_conflicting_versions_and_cross_tenant_edges() -> None:
    graph = AuthorityDerivationGraph(
        nodes=(
            AuthorityNode("subject:alice", "subject", tenant_id="tenant-a"),
            AuthorityNode("role:admin", "role", tenant_id="tenant-a"),
        ),
        edges=(
            AuthorityEdge("edge:v1", "subject:alice", "role:admin", "grant", (AuthorityScope("tenant-a", "client.read"),), policy_version="v1"),
            AuthorityEdge("edge:v2", "subject:alice", "role:admin", "grant", (AuthorityScope("tenant-a", "client.read"),), policy_version="v2"),
            AuthorityEdge("edge:tenant-b", "subject:alice", "role:admin", "grant", (AuthorityScope("tenant-b", "client.read"),), policy_version="v2"),
        ),
    )

    report = validate_authority_graph_integrity(graph)

    assert report.passed is False
    assert "conflicting policy versions for edge 'subject:alice'->'role:admin'" in report.failures
    assert "edge 'edge:tenant-b' scope crosses source tenant 'tenant-a'" in report.failures


def test_authority_graph_robustness_t2_multi_hop_attenuation_prevents_downstream_escalation() -> None:
    graph = AuthorityDerivationGraph(
        nodes=_nodes(),
        edges=(
            AuthorityEdge("edge:subject-role", "subject:alice", "role:admin", "assignment", (AuthorityScope("tenant-a", "client.read"),)),
            AuthorityEdge("edge:role-client", "role:admin", "authority:client", "grant", (AuthorityScope("tenant-a", "client.write"),)),
        ),
    )

    proof = graph.prove_reachability("subject:alice", AuthorityScope("tenant-a", "client.write"))

    assert proof.reachable is False
    assert tuple(scope.action for scope in compute_authority_closure(graph, "subject:alice").scopes) == ("client.read",)


def test_authority_graph_robustness_t2_outputs_are_deterministic_across_insertion_order() -> None:
    edges = (
        AuthorityEdge("edge:subject-role", "subject:alice", "role:admin", "assignment", (AuthorityScope("tenant-a", "client.*"),)),
        AuthorityEdge("edge:role-client", "role:admin", "authority:client", "grant", (AuthorityScope("tenant-a", "client.read"),)),
    )
    graph_a = AuthorityDerivationGraph(nodes=_nodes(), edges=edges)
    graph_b = AuthorityDerivationGraph(nodes=reversed(_nodes()), edges=reversed(edges))

    closure_a = compute_authority_closure(graph_a, "subject:alice")
    closure_b = compute_authority_closure(graph_b, "subject:alice")
    proof_a = graph_a.prove_reachability("subject:alice", AuthorityScope("tenant-a", "client.read"))
    proof_b = graph_b.prove_reachability("subject:alice", AuthorityScope("tenant-a", "client.read"))

    assert closure_a.scopes == closure_b.scopes
    assert tuple(path.edge_ids for path in proof_a.paths) == tuple(path.edge_ids for path in proof_b.paths)
