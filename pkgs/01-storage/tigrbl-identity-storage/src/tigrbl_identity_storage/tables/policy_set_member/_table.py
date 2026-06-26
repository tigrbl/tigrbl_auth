"""Durable policy set member records."""

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


class PolicySetMember(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "policy_set_members"
    __table_args__ = ({"schema": "authn"},)

    tenant_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    policy_set_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    member_kind: Mapped[str] = acol(storage=S(String(32), nullable=False, index=True))
    member_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    priority: Mapped[int] = acol(storage=S(Integer, nullable=False, default=0, index=True))
    condition_expression: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="active", index=True))
    member_metadata: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))


__all__ = ["PolicySetMember"]
