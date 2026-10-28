"""Owned mapped-table inventory."""

from .security_event_state import SecurityEvent, SecurityEventSubscription, SecurityEventDelivery, SecurityEventReplay

TABLE_MODELS = (
    SecurityEvent,
    SecurityEventSubscription,
    SecurityEventDelivery,
    SecurityEventReplay,
)
TABLE_MODEL_BY_NAME = {model.__name__: model for model in TABLE_MODELS}
TABLE_MODEL_BY_TABLENAME = {model.__tablename__: model for model in TABLE_MODELS}
__all__ = [model.__name__ for model in TABLE_MODELS] + [
    "TABLE_MODELS", "TABLE_MODEL_BY_NAME", "TABLE_MODEL_BY_TABLENAME",
]
