"""Durable access review decisions."""

from __future__ import annotations

from tigrbl_identity_storage.framework import (
    RestOltpTable,
    GUIDPk,
    Mapped,
    S,
    String,
    Timestamped,
    acol,
)


class AccessReviewDecision(RestOltpTable, GUIDPk, Timestamped):
    __tablename__ = "access_review_decisions"
    __table_args__ = ({"schema": "authn"},)

    decision_id: Mapped[str] = acol(storage=S(String(255), nullable=False, unique=True, index=True))
    item_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    reviewer_id: Mapped[str] = acol(storage=S(String(255), nullable=False, index=True))
    decision: Mapped[str] = acol(storage=S(String(64), nullable=False, index=True))
    reason: Mapped[str] = acol(storage=S(String(1000), nullable=False))


__all__ = ["AccessReviewDecision"]
