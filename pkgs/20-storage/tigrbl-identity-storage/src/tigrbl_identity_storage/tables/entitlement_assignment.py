"""Durable entitlement assignments."""

from __future__ import annotations

import datetime as dt
from typing import Any

from tigrbl_identity_storage.framework import Base, GUIDPk, Mapped, S, String, TZDateTime, Timestamped, acol

from ._ops import create_record, first_record, list_records, record_id, update_record


class EntitlementAssignment(Base, GUIDPk, Timestamped):
    __tablename__ = "entitlement_assignments"
    __table_args__ = ({"schema": "authn"},)

    assignment_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    entitlement_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    tenant_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    subject_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    justification: Mapped[str] = acol(storage=S(String(1000), nullable=False))
    assigned_by: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    expires_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="active", index=True))
    revoked_reason: Mapped[str | None] = acol(storage=S(String(1000), nullable=True))

    @classmethod
    async def assign(cls, db: Any, **payload: Any) -> "EntitlementAssignment":
        payload.setdefault("status", "active")
        return await create_record(cls, db, payload)

    @classmethod
    async def lookup(cls, db: Any, *, assignment_id: str) -> "EntitlementAssignment | None":
        return await first_record(cls, db, {"assignment_id": assignment_id})

    @classmethod
    async def list_for_subject(cls, db: Any, *, subject_id: str, tenant_id: str | None = None) -> list["EntitlementAssignment"]:
        filters: dict[str, Any] = {"subject_id": subject_id}
        if tenant_id is not None:
            filters["tenant_id"] = tenant_id
        return await list_records(cls, db, filters)

    @classmethod
    async def revoke(cls, db: Any, *, assignment_id: str, reason: str) -> "EntitlementAssignment | None":
        row = await cls.lookup(db, assignment_id=assignment_id)
        if row is None:
            return None
        return await update_record(
            cls,
            db,
            record_id(row),
            {"status": "revoked", "revoked_reason": reason},
        )


__all__ = ["EntitlementAssignment"]
