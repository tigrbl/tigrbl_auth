"""Durable security-event lifecycle operations."""

from tigrbl_identity_core.persistence import reject_sensitive_raw_fields
from tigrbl_identity_storage.tables import (
    SecurityEvent,
    SecurityEventDelivery,
    SecurityEventReplay,
    SecurityEventSubscription,
)

from tigrbl import provideTableHandler

record_security_event = provideTableHandler(
    SecurityEvent, payload_validator=reject_sensitive_raw_fields
)
record_security_event_subscription = provideTableHandler(
    SecurityEventSubscription, payload_validator=reject_sensitive_raw_fields
)
enqueue_security_event_delivery = provideTableHandler(
    SecurityEventDelivery, payload_validator=reject_sensitive_raw_fields
)
reserve_security_event_replay = provideTableHandler(
    SecurityEventReplay, payload_validator=reject_sensitive_raw_fields
)

__all__ = [
    "enqueue_security_event_delivery",
    "record_security_event",
    "record_security_event_subscription",
    "reserve_security_event_replay",
]
