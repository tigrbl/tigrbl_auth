"""Durable residency zones."""

from __future__ import annotations

from typing import Any

from tigrbl_identity_storage.framework import RestOltpTable, GUIDPk, JSON, Mapped, S, String, Timestamped, acol

from .._ops import create_record, first_record, list_records, record_id, update_record


class ResidencyZone(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "residency_zones"
    __table_args__ = ({"schema": "authn"},)

    zone_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    jurisdictions: Mapped[list] = acol(storage=S(JSON, nullable=False, default=list))
    sovereign_controls: Mapped[list | None] = acol(storage=S(JSON, nullable=True))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="active", index=True))

    @classmethod
    async def create_zone(cls, db: Any, **payload: Any) -> "ResidencyZone":
        payload.setdefault("status", "active")
        return await create_record(cls, db, payload)

    @classmethod
    async def lookup(cls, db: Any, *, zone_id: str) -> "ResidencyZone | None":
        return await first_record(cls, db, {"zone_id": zone_id})

    @classmethod
    async def list_active(cls, db: Any) -> list["ResidencyZone"]:
        return await list_records(cls, db, {"status": "active"})

    @classmethod
    async def disable(cls, db: Any, *, zone_id: str) -> "ResidencyZone | None":
        row = await cls.lookup(db, zone_id=zone_id)
        if row is None:
            return None
        return await update_record(cls, db, record_id(row), {"status": "disabled"})


__all__ = ["ResidencyZone"]
