"""Durable runtime qualification evidence."""

from __future__ import annotations

from typing import Any

from tigrbl_identity_storage.framework import RestOltpTable, GUIDPk, JSON, Mapped, S, String, Timestamped, acol

from .._ops import create_record, first_record, list_records


class RuntimeQualificationRecord(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "runtime_qualifications"
    __table_args__ = ({"schema": "authn"},)

    qualification_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    release_id: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    runtime_name: Mapped[str | None] = acol(storage=S(String(255), nullable=True, index=True))
    status: Mapped[str] = acol(storage=S(String(64), nullable=False, default="qualified", index=True))
    qualification_payload: Mapped[dict] = acol(storage=S(JSON, nullable=False, default=dict))

    @classmethod
    async def record(cls, db: Any, **payload: Any) -> "RuntimeQualificationRecord":
        payload.setdefault("qualification_payload", dict(payload))
        payload.setdefault("status", "qualified")
        return await create_record(cls, db, payload)

    @classmethod
    async def lookup(cls, db: Any, *, qualification_id: str) -> "RuntimeQualificationRecord | None":
        return await first_record(cls, db, {"qualification_id": qualification_id})

    @classmethod
    async def list_for_release(cls, db: Any, *, release_id: str) -> list["RuntimeQualificationRecord"]:
        return await list_records(cls, db, {"release_id": release_id})


__all__ = ["RuntimeQualificationRecord"]
