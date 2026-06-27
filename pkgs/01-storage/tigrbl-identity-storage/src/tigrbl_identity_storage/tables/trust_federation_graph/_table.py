"""Durable trust federation graph tables."""

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


class TrustFederationGraph(GraphBase, GUIDPk):
    __tablename__ = "trust_federation_graphs"
    __table_args__ = (
        UniqueConstraint("graph_key", name="uq_trust_federation_graph_key"),
        {"extend_existing": True, "schema": "authn"},
    )


class TrustFederationGraphNode(GraphNodeBase, GUIDPk):
    __tablename__ = "trust_federation_graph_nodes"
    __table_args__ = (
        UniqueConstraint("graph_id", "node_key", name="uq_trust_federation_graph_node_key"),
        Index("ix_trust_federation_graph_node_graph_kind", "graph_id", "kind"),
        Index("ix_trust_federation_graph_node_tenant_kind", "tenant_id", "kind"),
        {"extend_existing": True, "schema": "authn"},
    )

    graph_id: Mapped[UUID] = acol(
        storage=S(
            PgUUID(as_uuid=True),
            fk=ForeignKeySpec(target="authn.trust_federation_graphs.id"),
            nullable=False,
            index=True,
        )
    )
    issuers: Mapped[list | None] = acol(storage=S(JSON, nullable=True))
    clouds: Mapped[list | None] = acol(storage=S(JSON, nullable=True))
    identity_provider_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    federation_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))


class TrustFederationGraphEdge(GraphEdgeBase, GUIDPk):
    __tablename__ = "trust_federation_graph_edges"
    __table_args__ = (
        UniqueConstraint("graph_id", "edge_key", name="uq_trust_federation_graph_edge_key"),
        Index("ix_trust_federation_graph_edge_src_kind", "graph_id", "src_id", "kind"),
        Index("ix_trust_federation_graph_edge_dst_kind", "graph_id", "dst_id", "kind"),
        Index("ix_trust_federation_graph_edge_tenant_kind", "tenant_id", "kind"),
        {"extend_existing": True, "schema": "authn"},
    )

    graph_id: Mapped[UUID] = acol(
        storage=S(
            PgUUID(as_uuid=True),
            fk=ForeignKeySpec(target="authn.trust_federation_graphs.id"),
            nullable=False,
            index=True,
        )
    )
    src_id: Mapped[UUID] = acol(
        storage=S(
            PgUUID(as_uuid=True),
            fk=ForeignKeySpec(target="authn.trust_federation_graph_nodes.id"),
            nullable=False,
            index=True,
        )
    )
    dst_id: Mapped[UUID] = acol(
        storage=S(
            PgUUID(as_uuid=True),
            fk=ForeignKeySpec(target="authn.trust_federation_graph_nodes.id"),
            nullable=False,
            index=True,
        )
    )
    exchange_kind: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    constraints: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))


__all__ = [
    "TrustFederationGraph",
    "TrustFederationGraphNode",
    "TrustFederationGraphEdge",
]
