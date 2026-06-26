"""Durable policy set records for XACML-style policy grouping."""

from __future__ import annotations

from tigrbl_identity_storage.framework import (
    GUIDPk,
    Integer,
    JSON,
    Mapped,
    RestOltpTable,
    S,
    String,
    Timestamped,
    acol,
)


class PolicySet(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "policy_sets"
    __table_args__ = ({"schema": "authn"},)

    tenant_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    name: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    description: Mapped[str | None] = acol(storage=S(String(1000), nullable=True))
    combining_algorithm: Mapped[str] = acol(
        storage=S(String(128), nullable=False, default="deny_overrides", index=True)
    )
    priority: Mapped[int] = acol(storage=S(Integer, nullable=False, default=0, index=True))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="active", index=True))
    policy_set_metadata: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))


__all__ = ["PolicySet"]
