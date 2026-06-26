"""Durable policy target records."""

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


class PolicyTarget(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "policy_targets"
    __table_args__ = ({"schema": "authn"},)

    tenant_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    owner_kind: Mapped[str] = acol(storage=S(String(32), nullable=False, index=True))
    owner_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    subject_selector: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))
    resource_selector: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))
    action_selector: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))
    environment_selector: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))
    scope_selector: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))
    condition_expression: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))
    priority: Mapped[int] = acol(storage=S(Integer, nullable=False, default=0, index=True))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="active", index=True))
    target_metadata: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))


__all__ = ["PolicyTarget"]
