from __future__ import annotations

import tests.unit.formal_auth_helpers  # noqa: F401

from tigrbl_authz_policy_authority_derivation_graph import (
    AuthorityDerivationGraph,
    AuthorityEdge,
    AuthorityNode,
    AuthorityScope,
    compute_authority_closure,
    diff_least_authority,
)


def test_least_authority_diff_t1_attributes_excess_authority() -> None:
    graph = AuthorityDerivationGraph(
        nodes=(AuthorityNode("subject:alice", "subject"), AuthorityNode("authority:client", "authority")),
        edges=(
            AuthorityEdge(
                "edge:wide",
                "subject:alice",
                "authority:client",
                "grant",
                (AuthorityScope("tenant-a", "client.*"),),
            ),
        ),
    )

    diff = diff_least_authority(
        required=(AuthorityScope("tenant-a", "client.read"),),
        effective=compute_authority_closure(graph, "subject:alice"),
    )

    assert diff.passed is False
    assert tuple(scope.action for scope in diff.excess) == ("client.*",)
    assert diff.excess_provenance[("tenant-a", "", "client.*", "*")] == ("edge:wide",)
