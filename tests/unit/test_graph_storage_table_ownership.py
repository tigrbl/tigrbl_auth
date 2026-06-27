from __future__ import annotations

import importlib

from sqlalchemy import UniqueConstraint


def _unique_columns(model: type) -> set[tuple[str, ...]]:
    uniques: set[tuple[str, ...]] = set()
    for constraint in model.__table__.constraints:
        if isinstance(constraint, UniqueConstraint):
            uniques.add(tuple(column.name for column in constraint.columns))
    return uniques


def test_graph_storage_exports_concrete_graph_tables_not_generic_graph_registry() -> None:
    tables = importlib.import_module("tigrbl_identity_storage.tables")

    for abstract_name in ("GraphBase", "GraphNodeBase", "GraphEdgeBase"):
        assert abstract_name not in tables.TABLE_MODEL_BY_NAME

    for concrete_name in (
        "AuthorityDerivationGraph",
        "AuthorityDerivationGraphNode",
        "AuthorityDerivationGraphEdge",
        "TrustFederationGraph",
        "TrustFederationGraphNode",
        "TrustFederationGraphEdge",
    ):
        assert concrete_name in tables.TABLE_MODEL_BY_NAME
        assert getattr(tables, concrete_name) is tables.TABLE_MODEL_BY_NAME[concrete_name]


def test_graph_edge_uniqueness_is_edge_key_scoped_not_src_dst_kind() -> None:
    tables = importlib.import_module("tigrbl_identity_storage.tables")

    for model in (tables.AuthorityDerivationGraphEdge, tables.TrustFederationGraphEdge):
        uniques = _unique_columns(model)
        assert ("graph_id", "edge_key") in uniques
        assert ("src_id", "dst_id", "kind") not in uniques

    for model in (tables.AuthorityDerivationGraphNode, tables.TrustFederationGraphNode):
        assert ("graph_id", "node_key") in _unique_columns(model)


def test_authority_and_trust_graph_packages_bind_to_concrete_storage_tables() -> None:
    tables = importlib.import_module("tigrbl_identity_storage.tables")
    authority = importlib.import_module("tigrbl_authz_policy_authority_derivation_graph")
    trust = importlib.import_module("tigrbl_identity_admin_trust_federation_graph")

    assert authority.AuthorityDerivationGraph.graph_table is tables.AuthorityDerivationGraph
    assert authority.AuthorityDerivationGraph.node_table is tables.AuthorityDerivationGraphNode
    assert authority.AuthorityDerivationGraph.edge_table is tables.AuthorityDerivationGraphEdge
    assert trust.TrustFederationGraph.graph_table is tables.TrustFederationGraph
    assert trust.TrustFederationGraph.node_table is tables.TrustFederationGraphNode
    assert trust.TrustFederationGraph.edge_table is tables.TrustFederationGraphEdge


def test_graph_storage_does_not_introduce_repository_wrappers() -> None:
    forbidden_names = {
        "GraphRepository",
        "StorageGraphRepository",
        "AuthorityGraphRepository",
        "TrustGraphRepository",
    }
    modules = (
        importlib.import_module("tigrbl_identity_storage.tables"),
        importlib.import_module("tigrbl_authz_policy_authority_derivation_graph"),
        importlib.import_module("tigrbl_identity_admin_trust_federation_graph"),
    )

    for module in modules:
        for name in forbidden_names:
            assert not hasattr(module, name)
