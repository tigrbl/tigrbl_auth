"""Durable authority-graph table operations and specifications."""

from tigrbl_identity_storage.tables import (
    AuthorityDerivationGraph as AuthorityGraphTable,
    AuthorityDerivationGraphEdge as AuthorityGraphEdgeTable,
    AuthorityDerivationGraphNode as AuthorityGraphNodeTable,
)
from tigrbl_table_durability import (
    create_table_handler,
    deriveRuntimeTableSpec,
    makeRuntimeOperation,
)

record_authority_graph = create_table_handler(
    AuthorityGraphTable, reject_sensitive=False
)
add_authority_graph_node = create_table_handler(
    AuthorityGraphNodeTable, reject_sensitive=False
)
add_authority_graph_edge = create_table_handler(
    AuthorityGraphEdgeTable, reject_sensitive=False
)

AuthorityGraphRuntimeSpec = deriveRuntimeTableSpec(
    AuthorityGraphTable,
    operations=(
        makeRuntimeOperation(alias="record_graph", handler=record_authority_graph),
    ),
)
AuthorityGraphNodeRuntimeSpec = deriveRuntimeTableSpec(
    AuthorityGraphNodeTable,
    operations=(
        makeRuntimeOperation(alias="add_node", handler=add_authority_graph_node),
    ),
)
AuthorityGraphEdgeRuntimeSpec = deriveRuntimeTableSpec(
    AuthorityGraphEdgeTable,
    operations=(
        makeRuntimeOperation(alias="add_edge", handler=add_authority_graph_edge),
    ),
)

__all__ = [name for name in globals() if not name.startswith("_")]
