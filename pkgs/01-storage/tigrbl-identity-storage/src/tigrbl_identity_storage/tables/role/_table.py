"""Durable RBAC role definitions."""

from __future__ import annotations


from tigrbl_identity_storage.framework import RestOltpTable, GUIDPk, JSON, Mapped, S, String, Timestamped, acol



class Role(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "roles"
    __table_args__ = ({"schema": "authn"},)

    name: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    tenant_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    permissions: Mapped[list] = acol(storage=S(JSON, nullable=False, default=list))
    denied_permissions: Mapped[list | None] = acol(storage=S(JSON, nullable=True))
    inherited_roles: Mapped[list | None] = acol(storage=S(JSON, nullable=True))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="active", index=True))


__all__ = ["Role"]
