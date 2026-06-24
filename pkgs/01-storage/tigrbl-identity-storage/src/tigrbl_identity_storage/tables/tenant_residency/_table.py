"""Durable tenant residency assignments."""

from __future__ import annotations

from typing import Any

from tigrbl_identity_storage.framework import RestOltpTable, GUIDPk, JSON, Mapped, S, String, Timestamped, acol

from .._ops import create_record, first_record, record_id, update_record


class TenantResidency(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "tenant_residency"
    __table_args__ = ({"schema": "authn"},)

    tenant_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    residency_zone_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    allowed_processing_regions: Mapped[list] = acol(storage=S(JSON, nullable=False, default=list))
    restricted_transfer_regions: Mapped[list | None] = acol(storage=S(JSON, nullable=True))
    realm: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    residency_attributes: Mapped[dict | None] = acol(storage=S(JSON, nullable=True))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="active", index=True))

    @classmethod
    async def assign_residency(cls, db: Any, **payload: Any) -> "TenantResidency":
        existing = await cls.lookup(db, tenant_id=payload["tenant_id"])
        payload.setdefault("status", "active")
        if existing is not None:
            return await update_record(cls, db, record_id(existing), payload)
        return await create_record(cls, db, payload)

    @classmethod
    async def lookup(cls, db: Any, *, tenant_id: str) -> "TenantResidency | None":
        return await first_record(cls, db, {"tenant_id": tenant_id})

    @classmethod
    async def disable(cls, db: Any, *, tenant_id: str) -> "TenantResidency | None":
        row = await cls.lookup(db, tenant_id=tenant_id)
        if row is None:
            return None
        return await update_record(cls, db, record_id(row), {"status": "disabled"})


__all__ = ["TenantResidency"]
