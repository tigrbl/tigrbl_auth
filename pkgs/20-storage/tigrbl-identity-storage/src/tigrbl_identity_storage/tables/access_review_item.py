"""Durable access review campaign items."""

from __future__ import annotations

import datetime as dt
from typing import Any

from tigrbl_identity_storage.framework import RestOltpTable, GUIDPk, Integer, Mapped, S, String, TZDateTime, Timestamped, acol

from ._ops import create_record, first_record, list_records, record_id, update_record


class AccessReviewItem(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "access_review_items"
    __table_args__ = ({"schema": "authn"},)

    item_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    campaign_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    assignment_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    subject_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    entitlement_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    reviewer_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="pending", index=True))
    due_at: Mapped[dt.datetime] = acol(storage=S(TZDateTime, nullable=False, index=True))
    escalation_count: Mapped[int] = acol(storage=S(Integer, nullable=False, default=0))

    @classmethod
    async def create_item(cls, db: Any, **payload: Any) -> "AccessReviewItem":
        payload.setdefault("status", "pending")
        payload.setdefault("escalation_count", 0)
        return await create_record(cls, db, payload)

    @classmethod
    async def lookup(cls, db: Any, *, item_id: str) -> "AccessReviewItem | None":
        return await first_record(cls, db, {"item_id": item_id})

    @classmethod
    async def list_for_campaign(cls, db: Any, *, campaign_id: str) -> list["AccessReviewItem"]:
        return await list_records(cls, db, {"campaign_id": campaign_id})

    @classmethod
    async def mark_decided(cls, db: Any, *, item_id: str) -> "AccessReviewItem | None":
        row = await cls.lookup(db, item_id=item_id)
        if row is None:
            return None
        return await update_record(cls, db, record_id(row), {"status": "decided"})


__all__ = ["AccessReviewItem"]
