"""Durable RBAC role definitions."""

from __future__ import annotations

from typing import Any

from tigrbl_identity_storage.framework import Base, GUIDPk, JSON, Mapped, S, String, Timestamped, acol

from ._ops import create_record, first_record, list_records, record_id, update_record


class Role(Base, GUIDPk, Timestamped):
    __tablename__ = "roles"
    __table_args__ = ({"schema": "authn"},)

    name: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    tenant_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    permissions: Mapped[list] = acol(storage=S(JSON, nullable=False, default=list))
    denied_permissions: Mapped[list | None] = acol(storage=S(JSON, nullable=True))
    inherited_roles: Mapped[list | None] = acol(storage=S(JSON, nullable=True))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="active", index=True))

    @classmethod
    async def create_role(
        cls,
        db: Any,
        *,
        name: str,
        permissions: list[str] | tuple[str, ...],
        tenant_id: str | None = None,
        denied_permissions: list[str] | tuple[str, ...] = (),
        inherited_roles: list[str] | tuple[str, ...] = (),
    ) -> "Role":
        existing = await cls.lookup(db, name=name, tenant_id=tenant_id)
        payload = {
            "name": name,
            "tenant_id": tenant_id,
            "permissions": list(permissions),
            "denied_permissions": list(denied_permissions),
            "inherited_roles": list(inherited_roles),
            "status": "active",
        }
        if existing is not None:
            return await update_record(cls, db, record_id(existing), payload)
        return await create_record(cls, db, payload)

    @classmethod
    async def lookup(cls, db: Any, *, name: str, tenant_id: str | None = None) -> "Role | None":
        filters: dict[str, Any] = {"name": name}
        if tenant_id is not None:
            filters["tenant_id"] = tenant_id
        return await first_record(cls, db, filters)

    @classmethod
    async def list_for_tenant(cls, db: Any, *, tenant_id: str | None = None) -> list["Role"]:
        return await list_records(cls, db, {"tenant_id": tenant_id} if tenant_id is not None else {})

    @classmethod
    async def disable(cls, db: Any, *, name: str, tenant_id: str | None = None) -> "Role | None":
        row = await cls.lookup(db, name=name, tenant_id=tenant_id)
        if row is None:
            return None
        return await update_record(cls, db, record_id(row), {"status": "disabled"})


__all__ = ["Role"]
