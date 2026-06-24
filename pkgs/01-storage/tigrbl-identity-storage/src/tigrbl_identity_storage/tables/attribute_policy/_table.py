"""Durable ABAC policy definitions."""

from __future__ import annotations


from tigrbl_identity_storage.framework import RestOltpTable, GUIDPk, JSON, Mapped, S, String, Timestamped, acol



class AttributePolicy(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "attribute_policies"
    __table_args__ = ({"schema": "authn"},)

    name: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    tenant_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    client_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    permission: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    effect: Mapped[str] = acol(storage=S(String(32), nullable=False, default="allow", index=True))
    required_attributes: Mapped[dict] = acol(storage=S(JSON, nullable=False, default=dict))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="active", index=True))


__all__ = ["AttributePolicy"]
