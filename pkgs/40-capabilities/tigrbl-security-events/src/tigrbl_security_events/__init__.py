from collections.abc import Callable

from tigrbl_capability import Capability
from tigrbl_identity_contracts.capabilities import CapabilityMetadata
from tigrbl_identity_contracts.security_events import (
    SecurityEvent,
    SecurityEventReceiverPort,
    SecurityEventTransmitterPort,
)

EventRecorder = Callable[[str, SecurityEvent, str | None], None]


class SecurityEventsCapability(Capability):
    def __init__(
        self,
        transmitter: SecurityEventTransmitterPort,
        receiver: SecurityEventReceiverPort,
        recorder: EventRecorder | None = None,
    ):
        super().__init__(
            CapabilityMetadata(
                capability_id="security-events.delivery",
                version="1.0",
                operations=("transmit", "receive"),
                guarantees=("record-after-success",),
                optional_features=("event-recording",),
                dependencies=(type(transmitter).__name__, type(receiver).__name__),
            )
        )
        self._transmitter = transmitter
        self._receiver = receiver
        self._recorder = recorder
        self.bind("transmit", self.transmit, delegated=True)
        self.bind("receive", self.receive, delegated=True)

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
