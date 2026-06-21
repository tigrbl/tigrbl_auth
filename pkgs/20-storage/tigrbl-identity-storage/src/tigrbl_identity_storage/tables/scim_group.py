"""Durable SCIM group projection rows."""

from __future__ import annotations

from typing import Any

from tigrbl_identity_storage.framework import RestOltpTable, GUIDPk, JSON, Mapped, S, String, Timestamped, acol

from ._ops import create_record, first_record, list_records, record_id, update_record


class ScimGroupRecord(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "scim_groups"
    __table_args__ = ({"schema": "authn"},)

    group_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    tenant_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    display_name: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    members: Mapped[list] = acol(storage=S(JSON, nullable=False, default=list))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="active", index=True))

    @classmethod
    async def upsert_group(cls, db: Any, **payload: Any) -> "ScimGroupRecord":
        existing = await cls.lookup(db, group_id=payload["group_id"])
        payload.setdefault("status", "active")
        if existing is not None:
            return await update_record(cls, db, record_id(existing), payload)
        return await create_record(cls, db, payload)

    @classmethod
    async def lookup(cls, db: Any, *, group_id: str) -> "ScimGroupRecord | None":
        return await first_record(cls, db, {"group_id": group_id})

    @classmethod
    async def list_for_tenant(cls, db: Any, *, tenant_id: str) -> list["ScimGroupRecord"]:
        return await list_records(cls, db, {"tenant_id": tenant_id})

    @classmethod
    async def deactivate(cls, db: Any, *, group_id: str) -> "ScimGroupRecord | None":
        row = await cls.lookup(db, group_id=group_id)
        if row is None:
            return None
        return await update_record(cls, db, record_id(row), {"status": "disabled"})


__all__ = ["ScimGroupRecord"]
