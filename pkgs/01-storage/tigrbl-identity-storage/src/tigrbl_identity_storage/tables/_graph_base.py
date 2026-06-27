"""Shared abstract columns for graph-backed storage tables."""

from __future__ import annotations

from typing import Any

from tigrbl_identity_storage.framework import (
    Boolean,
    JSON,
    Mapped,
    RestOltpTable,
    S,
    String,
    Timestamped,
    acol,
)


class GraphBase(RestOltpTable, Timestamped):
    __abstract__ = True

    graph_key: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    tenant_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    realm: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="active", index=True))
    graph_metadata: Mapped[dict[str, Any] | None] = acol(storage=S(JSON, nullable=True))


class GraphNodeBase(RestOltpTable, Timestamped):
    __abstract__ = True

    node_key: Mapped[str] = acol(storage=S(String(1000), nullable=False, index=True))
    kind: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    tenant_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    realm: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    ref_table: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    ref_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    node_metadata: Mapped[dict[str, Any] | None] = acol(storage=S(JSON, nullable=True))


class GraphEdgeBase(RestOltpTable, Timestamped):
    __abstract__ = True

    edge_key: Mapped[str] = acol(storage=S(String(1000), nullable=False, index=True))
    kind: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    tenant_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    realm: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    active: Mapped[bool] = acol(storage=S(Boolean, nullable=False, default=True, index=True))
    revoked: Mapped[bool] = acol(storage=S(Boolean, nullable=False, default=False, index=True))
    edge_metadata: Mapped[dict[str, Any] | None] = acol(storage=S(JSON, nullable=True))


__all__ = ["GraphBase", "GraphNodeBase", "GraphEdgeBase"]
