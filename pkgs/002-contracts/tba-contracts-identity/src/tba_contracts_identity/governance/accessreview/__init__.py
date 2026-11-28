"""Access-review governance contract dataclasses."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AccessReviewItem:
    item_id: str
    assignment_id: str
    subject_id: str
    entitlement_id: str
    reviewer_id: str
    status: str
    due_at: str
    escalation_count: int = 0


@dataclass(frozen=True, slots=True)
class AccessReviewDecision:
    decision_id: str
    item_id: str
    reviewer_id: str
    decision: str
    reason: str
    recorded_at: str


@dataclass(frozen=True, slots=True)
class AccessReviewCampaign:
    campaign_id: str
    tenant_id: str
    name: str
    reviewer_ids: tuple[str, ...]
    item_ids: tuple[str, ...]
    created_at: str
    due_at: str
    closed_at: str | None = None
    status: str = "open"


__all__ = [
    "AccessReviewCampaign",
    "AccessReviewDecision",
    "AccessReviewItem",
]
