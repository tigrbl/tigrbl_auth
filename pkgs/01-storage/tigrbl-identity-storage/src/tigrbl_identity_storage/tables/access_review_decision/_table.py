"""Durable access review decisions."""

from __future__ import annotations

from typing import Any

from tigrbl_identity_storage.framework import RestOltpTable, GUIDPk, Mapped, S, String, Timestamped, acol

from .._ops import create_record, first_record, list_records


class AccessReviewDecision(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "access_review_decisions"
    __table_args__ = ({"schema": "authn"},)

    decision_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    item_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    reviewer_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    decision: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    reason: Mapped[str] = acol(storage=S(String(1000), nullable=False))

    @classmethod
    async def record_decision(cls, db: Any, **payload: Any) -> "AccessReviewDecision":
        return await create_record(cls, db, payload)

    @classmethod
    async def lookup(cls, db: Any, *, decision_id: str) -> "AccessReviewDecision | None":
        return await first_record(cls, db, {"decision_id": decision_id})

    @classmethod
    async def list_for_item(cls, db: Any, *, item_id: str) -> list["AccessReviewDecision"]:
        return await list_records(cls, db, {"item_id": item_id})


__all__ = ["AccessReviewDecision"]
