"""Durable release capability truth records."""

from __future__ import annotations

from typing import Any

from tigrbl_identity_storage.framework import RestOltpTable, GUIDPk, JSON, Mapped, S, String, Timestamped, acol

from .._ops import create_record, first_record, list_records, record_id, update_record


class ReleaseCapabilityRecord(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "release_capability_records"
    __table_args__ = ({"schema": "authn"},)

    capability_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    release_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    name: Mapped[str | None] = acol(storage=S(String(255), nullable=True))
    status: Mapped[str] = acol(storage=S(String(64), nullable=False, default="recorded", index=True))
    capability_payload: Mapped[dict] = acol(storage=S(JSON, nullable=False, default=dict))

    @classmethod
    async def record(cls, db: Any, **payload: Any) -> "ReleaseCapabilityRecord":
        existing = await cls.lookup(db, capability_id=payload["capability_id"])
        payload.setdefault("capability_payload", dict(payload))
        payload.setdefault("status", "recorded")
        if existing is not None:
            return await update_record(cls, db, record_id(existing), payload)
        return await create_record(cls, db, payload)

    @classmethod
    async def lookup(cls, db: Any, *, capability_id: str) -> "ReleaseCapabilityRecord | None":
        return await first_record(cls, db, {"capability_id": capability_id})

    @classmethod
    async def list_for_release(cls, db: Any, *, release_id: str) -> list["ReleaseCapabilityRecord"]:
        return await list_records(cls, db, {"release_id": release_id})


__all__ = ["ReleaseCapabilityRecord"]
