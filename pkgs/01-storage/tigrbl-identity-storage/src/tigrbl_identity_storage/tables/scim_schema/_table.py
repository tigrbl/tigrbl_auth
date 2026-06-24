"""Durable SCIM schema registry."""

from __future__ import annotations

from typing import Any

from tigrbl_identity_storage.framework import RestOltpTable, GUIDPk, JSON, Mapped, S, String, Timestamped, acol

from .._ops import create_record, first_record, record_id, update_record


class ScimSchemaRecord(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "scim_schemas"
    __table_args__ = ({"schema": "authn"},)

    schema_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    resource_kind: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    required_fields: Mapped[list] = acol(storage=S(JSON, nullable=False, default=list))
    schema_payload: Mapped[dict] = acol(storage=S(JSON, nullable=False, default=dict))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="active", index=True))

    @classmethod
    async def register_schema(cls, db: Any, **payload: Any) -> "ScimSchemaRecord":
        existing = await cls.lookup(db, schema_id=payload["schema_id"])
        payload.setdefault("schema_payload", dict(payload))
        payload.setdefault("status", "active")
        if existing is not None:
            return await update_record(cls, db, record_id(existing), payload)
        return await create_record(cls, db, payload)

    @classmethod
    async def lookup(cls, db: Any, *, schema_id: str) -> "ScimSchemaRecord | None":
        return await first_record(cls, db, {"schema_id": schema_id})

    @classmethod
    async def disable(cls, db: Any, *, schema_id: str) -> "ScimSchemaRecord | None":
        row = await cls.lookup(db, schema_id=schema_id)
        if row is None:
            return None
        return await update_record(cls, db, record_id(row), {"status": "disabled"})


__all__ = ["ScimSchemaRecord"]
