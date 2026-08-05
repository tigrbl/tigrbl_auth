"""Owned mapped-table inventory."""

from .access_review_campaign import AccessReviewCampaign
from .access_review_decision import AccessReviewDecision
from .access_review_item import AccessReviewItem
from .entitlement import Entitlement
from .entitlement_assignment import EntitlementAssignment

TABLE_MODELS = (
    Entitlement,
    EntitlementAssignment,
    AccessReviewCampaign,
    AccessReviewItem,
    AccessReviewDecision,
)
TABLE_MODEL_BY_NAME = {model.__name__: model for model in TABLE_MODELS}
TABLE_MODEL_BY_TABLENAME = {model.__tablename__: model for model in TABLE_MODELS}
__all__ = [model.__name__ for model in TABLE_MODELS] + [
    "TABLE_MODELS", "TABLE_MODEL_BY_NAME", "TABLE_MODEL_BY_TABLENAME",
]
