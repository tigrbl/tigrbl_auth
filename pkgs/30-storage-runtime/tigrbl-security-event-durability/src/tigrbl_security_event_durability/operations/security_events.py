"""Durable security-event lifecycle operations."""

from tigrbl_identity_storage.tables import (
    SecurityEvent,
    SecurityEventDelivery,
    SecurityEventReplay,
    SecurityEventSubscription,
)

from tigrbl_table_durability import create_table_handler

record_security_event = create_table_handler(SecurityEvent)
record_security_event_subscription = create_table_handler(SecurityEventSubscription)
enqueue_security_event_delivery = create_table_handler(SecurityEventDelivery)
reserve_security_event_replay = create_table_handler(SecurityEventReplay)

__all__ = [
    "enqueue_security_event_delivery",
    "record_security_event",
    "record_security_event_subscription",
    "reserve_security_event_replay",
]
