"""Durable entitlement definitions."""

from __future__ import annotations

from typing import Any

from tigrbl_identity_storage.framework import RestOltpTable, GUIDPk, Mapped, S, String, Timestamped, acol

from .._ops import create_record, first_record, list_records, record_id, update_record


class Entitlement(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "entitlements"
    __table_args__ = ({"schema": "authn"},)

    entitlement_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    tenant_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    name: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    owner: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    description: Mapped[str] = acol(storage=S(String(1000), nullable=False))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="active", index=True))

    @classmethod
    async def define(cls, db: Any, **payload: Any) -> "Entitlement":
        existing = await cls.lookup(db, entitlement_id=payload["entitlement_id"])
        payload.setdefault("status", "active")
        if existing is not None:
            return await update_record(cls, db, record_id(existing), payload)
        return await create_record(cls, db, payload)

    @classmethod
    async def lookup(cls, db: Any, *, entitlement_id: str) -> "Entitlement | None":
        return await first_record(cls, db, {"entitlement_id": entitlement_id})

    @classmethod
    async def list_for_tenant(cls, db: Any, *, tenant_id: str) -> list["Entitlement"]:
        return await list_records(cls, db, {"tenant_id": tenant_id})

    @classmethod
    async def disable(cls, db: Any, *, entitlement_id: str) -> "Entitlement | None":
        row = await cls.lookup(db, entitlement_id=entitlement_id)
        if row is None:
            return None
        return await update_record(cls, db, record_id(row), {"status": "disabled"})


__all__ = ["Entitlement"]
