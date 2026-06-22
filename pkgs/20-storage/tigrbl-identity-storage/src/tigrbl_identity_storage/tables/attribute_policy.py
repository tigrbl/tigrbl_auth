"""Durable ABAC policy definitions."""

from __future__ import annotations

from typing import Any

from tigrbl_identity_storage.framework import RestOltpTable, GUIDPk, JSON, Mapped, S, String, Timestamped, acol

from ._ops import create_record, first_record, list_records, record_id, update_record


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

    @classmethod
    async def create_policy(cls, db: Any, **payload: Any) -> "AttributePolicy":
        existing = await cls.lookup(db, name=payload["name"], tenant_id=payload.get("tenant_id"))
        payload.setdefault("status", "active")
        if existing is not None:
            return await update_record(cls, db, record_id(existing), payload)
        return await create_record(cls, db, payload)

    @classmethod
    async def lookup(cls, db: Any, *, name: str, tenant_id: str | None = None) -> "AttributePolicy | None":
        filters: dict[str, Any] = {"name": name}
        if tenant_id is not None:
            filters["tenant_id"] = tenant_id
        return await first_record(cls, db, filters)

    @classmethod
    async def list_for_permission(cls, db: Any, *, permission: str, tenant_id: str | None = None) -> list["AttributePolicy"]:
        filters: dict[str, Any] = {"permission": permission, "status": "active"}
        if tenant_id is not None:
            filters["tenant_id"] = tenant_id
        return await list_records(cls, db, filters)

    @classmethod
    async def list_active(cls, db: Any, *, tenant_id: str | None = None) -> list["AttributePolicy"]:
        filters: dict[str, Any] = {"status": "active"}
        if tenant_id is not None:
            filters["tenant_id"] = tenant_id
        return await list_records(cls, db, filters)

    @classmethod
    async def disable(cls, db: Any, *, name: str, tenant_id: str | None = None) -> "AttributePolicy | None":
        row = await cls.lookup(db, name=name, tenant_id=tenant_id)
        if row is None:
            return None
        return await update_record(cls, db, record_id(row), {"status": "disabled"})


__all__ = ["AttributePolicy"]
