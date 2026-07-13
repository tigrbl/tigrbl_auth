from collections.abc import Callable

from tigrbl_identity_contracts.security_events import (
    SecurityEvent,
    SecurityEventReceiverPort,
    SecurityEventTransmitterPort,
)

EventRecorder = Callable[[str, SecurityEvent, str | None], None]


class SecurityEventsCapability:
    def __init__(
        self,
        transmitter: SecurityEventTransmitterPort,
        receiver: SecurityEventReceiverPort,
        recorder: EventRecorder | None = None,
    ):
        self._transmitter = transmitter
        self._receiver = receiver
        self._recorder = recorder

    def transmit(self, event: SecurityEvent, subscriber: str) -> str:
        encoded = self._transmitter.transmit(event, subscriber)
        if self._recorder:
            self._recorder("transmitted", event, subscriber)
        return encoded

    def receive(self, encoded: str | bytes) -> SecurityEvent:
        event = self._receiver.receive(encoded)
        if self._recorder:
            self._recorder("received", event, None)
        return event


__all__ = ["EventRecorder", "SecurityEventsCapability"]
