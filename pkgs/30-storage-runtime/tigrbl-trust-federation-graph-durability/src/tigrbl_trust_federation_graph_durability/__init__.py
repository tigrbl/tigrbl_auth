"""Durable trust-federation graph table operations and specifications."""

from tigrbl_identity_storage.tables import (
    TrustFederationGraph as TrustFederationGraphTable,
    TrustFederationGraphEdge as TrustFederationGraphEdgeTable,
    TrustFederationGraphNode as TrustFederationGraphNodeTable,
)
from tigrbl_table_durability import (
    create_table_handler,
    deriveRuntimeTableSpec,
    makeRuntimeOperation,
)

record_trust_federation_graph = create_table_handler(
    TrustFederationGraphTable, reject_sensitive=False
)
add_trust_federation_graph_node = create_table_handler(
    TrustFederationGraphNodeTable, reject_sensitive=False
)
add_trust_federation_graph_edge = create_table_handler(
    TrustFederationGraphEdgeTable, reject_sensitive=False
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
    TrustFederationGraphNodeTable,
    operations=(
        makeRuntimeOperation(alias="add_node", handler=add_trust_federation_graph_node),
    ),
)
TrustFederationGraphEdgeRuntimeSpec = deriveRuntimeTableSpec(
    TrustFederationGraphEdgeTable,
    operations=(
        makeRuntimeOperation(alias="add_edge", handler=add_trust_federation_graph_edge),
    ),
)

__all__ = [name for name in globals() if not name.startswith("_")]
