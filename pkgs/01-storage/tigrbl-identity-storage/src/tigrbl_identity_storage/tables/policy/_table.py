"""Durable policy definition records for PAP and PRP surfaces."""

from __future__ import annotations

from tigrbl_identity_storage.framework import (
    GUIDPk,
    JSON,
    Mapped,
    RestOltpTable,
    S,
    String,
    Timestamped,
    acol,
)


class Policy(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "policies"
    __table_args__ = ({"schema": "authn"},)

    tenant_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    name: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    language: Mapped[str] = acol(storage=S(String(128), nullable=False, default="tigrbl-conditions/v1", index=True))
    description: Mapped[str | None] = acol(storage=S(String(1000), nullable=True))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="draft", index=True))
    active_version_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    policy_metadata: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))


__all__ = ["Policy"]
