"""Durable authority-graph table runtime with compatibility re-exports."""

from tigrbl_authority_graph_concrete import *
from tigrbl_authority_graph_concrete import __all__ as _concrete_exports
from tigrbl_identity_storage.tables import (
    AuthorityDerivationGraph as AuthorityDerivationGraphTable,
    AuthorityDerivationGraphEdge,
    AuthorityDerivationGraphNode,
)
from tigrbl_identity_storage_runtime import (
    create_table_handler,
    deriveRuntimeTableSpec,
    makeRuntimeOperation,
)

record_authority_graph = create_table_handler(
    AuthorityDerivationGraphTable, reject_sensitive=False
)
add_authority_graph_node = create_table_handler(
    AuthorityDerivationGraphNode, reject_sensitive=False
)
add_authority_graph_edge = create_table_handler(
    AuthorityDerivationGraphEdge, reject_sensitive=False
)

AuthorityDerivationGraphRuntimeSpec = deriveRuntimeTableSpec(
    AuthorityDerivationGraphTable,
    operations=(
        makeRuntimeOperation(
            alias="record_graph", handler=record_authority_graph
        ),
    ),
)
AuthorityDerivationGraphNodeRuntimeSpec = deriveRuntimeTableSpec(
    AuthorityDerivationGraphNode,
    operations=(
        makeRuntimeOperation(
            alias="add_node", handler=add_authority_graph_node
        ),
    ),
)
AuthorityDerivationGraphEdgeRuntimeSpec = deriveRuntimeTableSpec(
    AuthorityDerivationGraphEdge,
    operations=(
        makeRuntimeOperation(
            alias="add_edge", handler=add_authority_graph_edge
        ),
    ),
)

__all__ = [
    *_concrete_exports,
    "AuthorityDerivationGraphTable",
    "AuthorityDerivationGraphNode",
    "AuthorityDerivationGraphEdge",
    "AuthorityDerivationGraphRuntimeSpec",
    "AuthorityDerivationGraphNodeRuntimeSpec",
    "AuthorityDerivationGraphEdgeRuntimeSpec",
    "record_authority_graph",
    "add_authority_graph_node",
    "add_authority_graph_edge",
]
