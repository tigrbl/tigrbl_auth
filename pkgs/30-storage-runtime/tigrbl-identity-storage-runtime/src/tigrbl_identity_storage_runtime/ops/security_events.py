"""Durable security-event lifecycle operations."""

from tigrbl_identity_storage.tables import (
    SecurityEvent,
    SecurityEventDelivery,
    SecurityEventReplay,
)

from .common import create_table_handler

record_security_event = create_table_handler(SecurityEvent)
enqueue_security_event_delivery = create_table_handler(SecurityEventDelivery)
reserve_security_event_replay = create_table_handler(SecurityEventReplay)

__all__ = [
    "enqueue_security_event_delivery",
    "record_security_event",
    "reserve_security_event_replay",
]
