from abc import ABC

from tigrbl_security_event_contracts import (
    SecurityEvent,
    SecurityEventReceiverPort,
    SecurityEventTransmitterPort,
)


class SecurityEventTransmitterBase(SecurityEventTransmitterPort, ABC):
    def transmit(self, event: SecurityEvent, subscriber: str, /) -> str:
        raise NotImplementedError


class SecurityEventReceiverBase(SecurityEventReceiverPort, ABC):
    def receive(self, encoded_event: str | bytes, /) -> SecurityEvent:
        raise NotImplementedError


class SecurityEventDeliveryBase(ABC):
    def deliver(self, encoded_event: str | bytes, subscriber: str, /) -> bool:
        raise NotImplementedError


class SecurityEventReplayBase(ABC):
    def consume_once(self, issuer: str, token_id: str, /) -> bool:
        raise NotImplementedError


__all__ = [
    "SecurityEventDeliveryBase",
    "SecurityEventReceiverBase",
    "SecurityEventReplayBase",
    "SecurityEventTransmitterBase",
]
