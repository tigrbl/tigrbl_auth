"""Durable authority derivation graph tables."""

from __future__ import annotations

from sqlalchemy import Index, UniqueConstraint

from tigrbl_identity_storage.framework import (
    ForeignKeySpec,
    GUIDPk,
    JSON,
    Mapped,
    PgUUID,
    S,
    String,
    UUID,
    acol,
)
from tigrbl_identity_storage.tables._graph_base import GraphBase, GraphEdgeBase, GraphNodeBase


class AuthorityDerivationGraph(GraphBase, GUIDPk):
    __tablename__ = "authority_derivation_graphs"
    __table_args__ = (
        UniqueConstraint("graph_key", name="uq_authority_derivation_graph_key"),
        {"extend_existing": True, "schema": "authn"},
    )


class AuthorityDerivationGraphNode(GraphNodeBase, GUIDPk):
    __tablename__ = "authority_derivation_graph_nodes"
    __table_args__ = (
        UniqueConstraint("graph_id", "node_key", name="uq_authority_derivation_graph_node_key"),
        Index("ix_authority_derivation_graph_node_graph_kind", "graph_id", "kind"),
        Index("ix_authority_derivation_graph_node_tenant_kind", "tenant_id", "kind"),
        {"extend_existing": True, "schema": "authn"},
    )

    graph_id: Mapped[UUID] = acol(
        storage=S(
            PgUUID(as_uuid=True),
            fk=ForeignKeySpec(target="authn.authority_derivation_graphs.id"),
            nullable=False,
            index=True,
        )
    )


class AuthorityDerivationGraphEdge(GraphEdgeBase, GUIDPk):
    __tablename__ = "authority_derivation_graph_edges"
    __table_args__ = (
        UniqueConstraint("graph_id", "edge_key", name="uq_authority_derivation_graph_edge_key"),
        Index("ix_authority_derivation_graph_edge_src_kind", "graph_id", "src_id", "kind"),
        Index("ix_authority_derivation_graph_edge_dst_kind", "graph_id", "dst_id", "kind"),
        Index("ix_authority_derivation_graph_edge_tenant_kind", "tenant_id", "kind"),
        {"extend_existing": True, "schema": "authn"},
    )

    graph_id: Mapped[UUID] = acol(
        storage=S(
            PgUUID(as_uuid=True),
            fk=ForeignKeySpec(target="authn.authority_derivation_graphs.id"),
            nullable=False,
            index=True,
        )
    )
    src_id: Mapped[UUID] = acol(
        storage=S(
            PgUUID(as_uuid=True),
            fk=ForeignKeySpec(target="authn.authority_derivation_graph_nodes.id"),
            nullable=False,
            index=True,
        )
    )
    dst_id: Mapped[UUID] = acol(
        storage=S(
            PgUUID(as_uuid=True),
            fk=ForeignKeySpec(target="authn.authority_derivation_graph_nodes.id"),
            nullable=False,
            index=True,
        )
    )
    policy_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    policy_version_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    policy_version: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    provenance_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    scopes: Mapped[list | None] = acol(storage=S(JSON, nullable=True))
    constraints: Mapped[list | None] = acol(storage=S(JSON, nullable=True))


__all__ = [
    "AuthorityDerivationGraph",
    "AuthorityDerivationGraphNode",
    "AuthorityDerivationGraphEdge",
]
