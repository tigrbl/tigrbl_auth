"""Durable access review campaigns."""

from __future__ import annotations

import datetime as dt
from typing import Any

from tigrbl_identity_storage.framework import RestOltpTable, GUIDPk, JSON, Mapped, S, String, TZDateTime, Timestamped, acol

from .._ops import create_record, first_record, list_records, record_id, update_record, utc_now


class AccessReviewCampaign(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "access_review_campaigns"
    __table_args__ = ({"schema": "authn"},)

    campaign_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    tenant_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    name: Mapped[str] = acol(storage=S(String(255), nullable=False))
    reviewer_ids: Mapped[list] = acol(storage=S(JSON, nullable=False, default=list))
    item_ids: Mapped[list | None] = acol(storage=S(JSON, nullable=True))
    due_at: Mapped[dt.datetime] = acol(storage=S(TZDateTime, nullable=False, index=True))
    closed_at: Mapped[dt.datetime | None] = acol(storage=S(TZDateTime, nullable=True, index=True))
    status: Mapped[str] = acol(storage=S(String(32), nullable=False, default="open", index=True))

    @classmethod
    async def create_campaign(cls, db: Any, **payload: Any) -> "AccessReviewCampaign":
        payload.setdefault("status", "open")
        return await create_record(cls, db, payload)

    @classmethod
    async def lookup(cls, db: Any, *, campaign_id: str) -> "AccessReviewCampaign | None":
        return await first_record(cls, db, {"campaign_id": campaign_id})

    @classmethod
    async def list_for_tenant(cls, db: Any, *, tenant_id: str, status: str | None = None) -> list["AccessReviewCampaign"]:
        filters: dict[str, Any] = {"tenant_id": tenant_id}
        if status is not None:
            filters["status"] = status
        return await list_records(cls, db, filters)

    @classmethod
    async def close(cls, db: Any, *, campaign_id: str) -> "AccessReviewCampaign | None":
        row = await cls.lookup(db, campaign_id=campaign_id)
        if row is None:
            return None
        return await update_record(cls, db, record_id(row), {"status": "closed", "closed_at": utc_now()})


__all__ = ["AccessReviewCampaign"]
