"""Durable access review campaign items."""

from __future__ import annotations

import datetime as dt

from tigrbl_identity_storage.framework import RestOltpTable, GUIDPk, Integer, Mapped, S, String, TZDateTime, Timestamped, acol



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


__all__ = ["AccessReviewItem"]
