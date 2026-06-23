"""Durable SCIM user projection rows."""

from __future__ import annotations

from typing import Any

from tigrbl_identity_storage.framework import RestOltpTable, GUIDPk, JSON, Mapped, S, String, Timestamped, acol

from ._ops import create_record, first_record, list_records, record_id, update_record


class ScimUserRecord(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "scim_users"
    __table_args__ = ({"schema": "authn"},)

    user_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    tenant_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    user_name: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    attributes: Mapped[dict] = acol(storage=S(JSON, nullable=False, default=dict))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="active", index=True))

    @classmethod
    async def upsert_user(cls, db: Any, **payload: Any) -> "ScimUserRecord":
        existing = await cls.lookup(db, user_id=payload["user_id"])
        payload.setdefault("status", "active" if payload.get("active", True) else "disabled")
        if existing is not None:
            return await update_record(cls, db, record_id(existing), payload)
        return await create_record(cls, db, payload)

    @classmethod
    async def lookup(cls, db: Any, *, user_id: str) -> "ScimUserRecord | None":
        return await first_record(cls, db, {"user_id": user_id})

    @classmethod
    async def list_for_tenant(cls, db: Any, *, tenant_id: str) -> list["ScimUserRecord"]:
        return await list_records(cls, db, {"tenant_id": tenant_id})

    @classmethod
    async def deactivate(cls, db: Any, *, user_id: str) -> "ScimUserRecord | None":
        row = await cls.lookup(db, user_id=user_id)
        if row is None:
            return None
        return await update_record(cls, db, record_id(row), {"status": "disabled"})


__all__ = ["ScimUserRecord"]
