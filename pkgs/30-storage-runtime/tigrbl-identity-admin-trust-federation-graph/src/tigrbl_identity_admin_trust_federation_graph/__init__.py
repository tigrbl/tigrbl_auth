"""Durable trust-federation graph runtime with compatibility re-exports."""

from tigrbl_identity_storage.tables import (
    TrustFederationGraph as TrustFederationGraphTable,
    TrustFederationGraphEdge,
    TrustFederationGraphNode,
)
from tigrbl_identity_storage_runtime import (
    create_table_handler,
    deriveRuntimeTableSpec,
    makeRuntimeOperation,
)
from tigrbl_trust_federation_graph_concrete import *
from tigrbl_trust_federation_graph_concrete import __all__ as _concrete_exports

record_trust_federation_graph = create_table_handler(
    TrustFederationGraphTable, reject_sensitive=False
)
add_trust_federation_graph_node = create_table_handler(
    TrustFederationGraphNode, reject_sensitive=False
)
add_trust_federation_graph_edge = create_table_handler(
    TrustFederationGraphEdge, reject_sensitive=False
)

TrustFederationGraphRuntimeSpec = deriveRuntimeTableSpec(
    TrustFederationGraphTable,
    operations=(
        makeRuntimeOperation(
            alias="record_graph", handler=record_trust_federation_graph
        ),
    ),
)
TrustFederationGraphNodeRuntimeSpec = deriveRuntimeTableSpec(
    TrustFederationGraphNode,
    operations=(
        makeRuntimeOperation(
            alias="add_node", handler=add_trust_federation_graph_node
        ),
    ),
)
TrustFederationGraphEdgeRuntimeSpec = deriveRuntimeTableSpec(
    TrustFederationGraphEdge,
    operations=(
        makeRuntimeOperation(
            alias="add_edge", handler=add_trust_federation_graph_edge
        ),
    ),
)

__all__ = [
    *_concrete_exports,
    "TrustFederationGraphTable",
    "TrustFederationGraphNode",
    "TrustFederationGraphEdge",
    "TrustFederationGraphRuntimeSpec",
    "TrustFederationGraphNodeRuntimeSpec",
    "TrustFederationGraphEdgeRuntimeSpec",
    "record_trust_federation_graph",
    "add_trust_federation_graph_node",
    "add_trust_federation_graph_edge",
]
