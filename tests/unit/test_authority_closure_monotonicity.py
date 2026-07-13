from __future__ import annotations

import tests.unit.formal_auth_helpers  # noqa: F401

from tigrbl_authz_policy_authority_derivation_graph import (
    AuthorityDerivationGraph,
    AuthorityEdge,
    AuthorityMutationKind,
    AuthorityNode,
    AuthorityScope,
    compare_authority_monotonicity,
    compute_authority_closure,
)


def test_authority_closure_t1_computes_effective_scopes_and_provenance() -> None:
    graph = AuthorityDerivationGraph(
        nodes=(
            AuthorityNode("subject:bob", "subject"),
            AuthorityNode("authority:client", "authority"),
        ),
        edges=(
            AuthorityEdge(
                "edge:client-read",
                "subject:bob",
                "authority:client",
                "direct-grant",
                (AuthorityScope("tenant-a", "client.read"),),
            ),
        ),
    )

    closure = compute_authority_closure(graph, "subject:bob")

    assert tuple(scope.action for scope in closure.scopes) == ("client.read",)
    assert closure.provenance[("tenant-a", "", "client.read", "*")] == (
        "edge:client-read",
    )


def test_authority_monotonicity_t1_detects_revoke_expansion() -> None:
    before_graph = AuthorityDerivationGraph(
        nodes=(
            AuthorityNode("subject:bob", "subject"),
            AuthorityNode("authority:client", "authority"),
        ),
        edges=(
            AuthorityEdge(
                "edge:read",
                "subject:bob",
                "authority:client",
                "grant",
                (AuthorityScope("tenant-a", "client.read"),),
            ),
        ),
    )
    after_graph = AuthorityDerivationGraph(
        nodes=(
            AuthorityNode("subject:bob", "subject"),
            AuthorityNode("authority:client", "authority"),
        ),
        edges=(
            AuthorityEdge(
                "edge:read",
                "subject:bob",
                "authority:client",
                "grant",
                (AuthorityScope("tenant-a", "client.read"),),
            ),
            AuthorityEdge(
                "edge:write",
                "subject:bob",
                "authority:client",
                "grant",
                (AuthorityScope("tenant-a", "client.write"),),
            ),
        ),
    )

    report = compare_authority_monotonicity(
        compute_authority_closure(before_graph, "subject:bob"),
        compute_authority_closure(after_graph, "subject:bob"),
        mutation_kind=AuthorityMutationKind.REVOKE,
    )

    assert report.passed is False
    assert tuple(scope.action for scope in report.added) == ("client.write",)
    assert report.failures == ("revoke mutation added authority",)
