"""Durable plugin descriptor registry."""

from __future__ import annotations

from typing import Any

from tigrbl_identity_storage.framework import Base, GUIDPk, JSON, Mapped, S, String, Timestamped, acol

from ._ops import create_record, first_record, list_records, record_id, update_record


class PluginDescriptorRecord(Base, GUIDPk, Timestamped):
    __tablename__ = "plugin_descriptors"
    __table_args__ = ({"schema": "authn"},)

    plugin_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    name: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    version: Mapped[str] = acol(storage=S(String(128), nullable=False))
    isolation_mode: Mapped[str] = acol(storage=S(String(64), nullable=False))
    fail_behavior: Mapped[str] = acol(storage=S(String(64), nullable=False))
    descriptor_payload: Mapped[dict] = acol(storage=S(JSON, nullable=False, default=dict))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="enabled", index=True))

    @classmethod
    async def register(cls, db: Any, **payload: Any) -> "PluginDescriptorRecord":
        existing = await cls.lookup(db, plugin_id=payload["plugin_id"])
        payload.setdefault("descriptor_payload", dict(payload))
        payload.setdefault("status", "enabled" if payload.get("enabled", True) else "disabled")
        if existing is not None:
            return await update_record(cls, db, record_id(existing), payload)
        return await create_record(cls, db, payload)

    @classmethod
    async def lookup(cls, db: Any, *, plugin_id: str) -> "PluginDescriptorRecord | None":
        return await first_record(cls, db, {"plugin_id": plugin_id})

    @classmethod
    async def list_enabled(cls, db: Any) -> list["PluginDescriptorRecord"]:
        return await list_records(cls, db, {"status": "enabled"})

    @classmethod
    async def disable(cls, db: Any, *, plugin_id: str) -> "PluginDescriptorRecord | None":
        row = await cls.lookup(db, plugin_id=plugin_id)
        if row is None:
            return None
        return await update_record(cls, db, record_id(row), {"status": "disabled"})


__all__ = ["PluginDescriptorRecord"]
