"""Durable entitlement definitions."""

from __future__ import annotations


from tigrbl_identity_storage.framework import RestOltpTable, GUIDPk, Mapped, S, String, Timestamped, acol



class Entitlement(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "entitlements"
    __table_args__ = ({"schema": "authn"},)

    entitlement_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    tenant_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    name: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    owner: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    description: Mapped[str] = acol(storage=S(String(1000), nullable=False))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="active", index=True))


__all__ = ["Entitlement"]
