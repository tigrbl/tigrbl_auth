"""Durable SDK package catalog."""

from __future__ import annotations

from typing import Any

from tigrbl_identity_storage.framework import Base, GUIDPk, JSON, Mapped, S, String, Timestamped, acol

from ._ops import create_record, first_record, list_records, record_id, update_record


class SDKPackageRecord(Base, GUIDPk, Timestamped):
    __tablename__ = "sdk_packages"
    __table_args__ = ({"schema": "authn"},)

    sdk_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    package_name: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    language: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    version: Mapped[str] = acol(storage=S(String(128), nullable=False, index=True))
    release_channel: Mapped[str] = acol(storage=S(String(64), nullable=False, default="stable", index=True))
    contract_payload: Mapped[dict] = acol(storage=S(JSON, nullable=False, default=dict))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="active", index=True))

    @classmethod
    async def register(cls, db: Any, **payload: Any) -> "SDKPackageRecord":
        existing = await cls.lookup(db, sdk_id=payload["sdk_id"])
        payload.setdefault("release_channel", "stable")
        payload.setdefault("contract_payload", dict(payload))
        payload.setdefault("status", "active")
        if existing is not None:
            return await update_record(cls, db, record_id(existing), payload)
        return await create_record(cls, db, payload)

    @classmethod
    async def lookup(cls, db: Any, *, sdk_id: str) -> "SDKPackageRecord | None":
        return await first_record(cls, db, {"sdk_id": sdk_id})

    @classmethod
    async def list_by_language(cls, db: Any, *, language: str) -> list["SDKPackageRecord"]:
        return await list_records(cls, db, {"language": language})

    @classmethod
    async def disable(cls, db: Any, *, sdk_id: str) -> "SDKPackageRecord | None":
        row = await cls.lookup(db, sdk_id=sdk_id)
        if row is None:
            return None
        return await update_record(cls, db, record_id(row), {"status": "disabled"})


__all__ = ["SDKPackageRecord"]
