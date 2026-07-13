from tigrbl_identity_storage.tables.security_event import SecurityEvent
from tigrbl_identity_storage.tables.security_event_delivery import SecurityEventDelivery
from tigrbl_identity_storage.tables.security_event_replay import SecurityEventReplay

from .repositories import DurableRepository


class SecurityEventRepository(DurableRepository):
    table = SecurityEvent


class SecurityEventDeliveryRepository(DurableRepository):
    table = SecurityEventDelivery


class SecurityEventReplayRepository(DurableRepository):
    table = SecurityEventReplay


__all__ = [
    "SecurityEventDeliveryRepository",
    "SecurityEventReplayRepository",
    "SecurityEventRepository",
]
