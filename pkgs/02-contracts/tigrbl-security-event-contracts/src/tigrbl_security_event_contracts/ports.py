"""Canonical security-event delivery ports."""

from typing import Protocol

from .events import SecurityEvent


class SecurityEventTransmitterPort(Protocol):
    def transmit(self, event: SecurityEvent, subscriber: str, /) -> str: ...


class SecurityEventReceiverPort(Protocol):
    def receive(self, encoded_event: str | bytes, /) -> SecurityEvent: ...


__all__ = ["SecurityEventReceiverPort", "SecurityEventTransmitterPort"]
