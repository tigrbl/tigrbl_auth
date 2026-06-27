from __future__ import annotations

import tests.unit.formal_auth_helpers  # noqa: F401

from tigrbl_auth.services.formal_authorization import AuthorityDerivationGraph as FacadeGraph
from tigrbl_authz_policy import AuthorityDerivationGraph as PolicyGraph
from tigrbl_identity_storage.tables import (
    AuthorityDerivationGraph as AuthorityDerivationGraphTable,
    AuthorityDerivationGraphEdge,
    AuthorityDerivationGraphNode,
)
from tigrbl_authz_policy_authority_derivation_graph import (
    AuthorityDerivationGraph,
    AuthorityEdge,
    AuthorityNode,
    AuthorityScope,
)


def _graph() -> AuthorityDerivationGraph:
    return AuthorityDerivationGraph(
        nodes=(
            AuthorityNode("subject:alice", "subject", tenant_id="tenant-a", realm="realm-a"),
            AuthorityNode("role:admin", "role", tenant_id="tenant-a", realm="realm-a"),
            AuthorityNode("authority:client", "authority", tenant_id="tenant-a", realm="realm-a"),
        ),
        edges=(
            AuthorityEdge(
                "edge:assignment",
                "subject:alice",
                "role:admin",
                "assignment",
                (AuthorityScope("tenant-a", "client.*", realm="realm-a"),),
                policy_version="v1",
            ),
            AuthorityEdge(
                "edge:role",
                "role:admin",
                "authority:client",
                "role-grant",
                (AuthorityScope("tenant-a", "client.read", realm="realm-a"),),
                provenance_id="prov:role",
            ),
        ),
    )


def test_authority_derivation_graph_t0_exports_facade_identity() -> None:
    assert FacadeGraph is AuthorityDerivationGraph
    assert PolicyGraph is AuthorityDerivationGraph
    assert AuthorityDerivationGraph.graph_table is AuthorityDerivationGraphTable
    assert AuthorityDerivationGraph.node_table is AuthorityDerivationGraphNode
    assert AuthorityDerivationGraph.edge_table is AuthorityDerivationGraphEdge


def test_authority_derivation_graph_t1_derives_paths_and_reachability() -> None:
    graph = _graph()

    paths = graph.derive_paths("subject:alice")
    proof = graph.prove_reachability("subject:alice", AuthorityScope("tenant-a", "client.read", realm="realm-a"))

    assert tuple(path.edge_ids for path in paths) == (("edge:assignment", "edge:role"), ("edge:assignment",))
    assert proof.reachable is True
    assert tuple(path.target for path in proof.paths) == ("authority:client", "role:admin")
    assert graph.prove_reachability("subject:alice", AuthorityScope("tenant-b", "client.read")).reachable is False
