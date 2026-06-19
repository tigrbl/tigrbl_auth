"""Append-only SCIM patch operation events."""

from __future__ import annotations

from typing import Any

from tigrbl_identity_storage.framework import Base, GUIDPk, JSON, Mapped, S, String, Timestamped, acol

from ._ops import create_record, list_records


class ScimPatchEvent(Base, GUIDPk, Timestamped):
    __tablename__ = "scim_patch_events"
    __table_args__ = ({"schema": "authn"},)

    tenant_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    resource_kind: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    resource_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    op: Mapped[str] = acol(storage=S(String(64), nullable=False))
    path: Mapped[str | None] = acol(storage=S(String(512), nullable=True))
    value_payload: Mapped[dict | list | str | int | float | bool | None] = acol(storage=S(JSON, nullable=True))

    @classmethod
    async def append_event(cls, db: Any, **payload: Any) -> "ScimPatchEvent":
        return await create_record(cls, db, payload)

    @classmethod
    async def list_for_resource(cls, db: Any, *, resource_kind: str, resource_id: str) -> list["ScimPatchEvent"]:
        return await list_records(cls, db, {"resource_kind": resource_kind, "resource_id": resource_id})

    @classmethod
    async def list_for_tenant(cls, db: Any, *, tenant_id: str) -> list["ScimPatchEvent"]:
        return await list_records(cls, db, {"tenant_id": tenant_id})


__all__ = ["ScimPatchEvent"]
