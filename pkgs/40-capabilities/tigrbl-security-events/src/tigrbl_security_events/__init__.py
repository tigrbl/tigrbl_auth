"""Composable security-event delivery over injected durable operations."""

from __future__ import annotations

import inspect
from collections.abc import Callable
from datetime import datetime, timezone
from typing import TypeAlias

from tigrbl_capability import Capability
from tigrbl_identity_contracts.capabilities import (
    CapabilityDefinition,
    CapabilityOperation,
)
from tigrbl_identity_contracts.security_events import (
    SecurityEvent,
    SecurityEventDelivery,
    SecurityEventReceiverPort,
    SecurityEventSubscription,
    SecurityEventTransmitterPort,
)

EventRecorder: TypeAlias = Callable[[SecurityEvent], object]
SubscriptionResolver: TypeAlias = Callable[
    [str, SecurityEvent], SecurityEventSubscription | None | object
]
DeliveryRecorder: TypeAlias = Callable[[SecurityEventDelivery], object]
ReplayReserver: TypeAlias = Callable[[SecurityEvent], object]


async def _resolve(value):
    return await value if inspect.isawaitable(value) else value


class SecurityEventsCapability(Capability):
    def __init__(
        self,
        transmitter: SecurityEventTransmitterPort,
        receiver: SecurityEventReceiverPort,
        event_recorder: EventRecorder,
        subscription_resolver: SubscriptionResolver,
        delivery_recorder: DeliveryRecorder,
        replay_reserver: ReplayReserver,
    ):
        self._transmitter = transmitter
        self._receiver = receiver
        self._event_recorder = event_recorder
        self._subscription_resolver = subscription_resolver
        self._delivery_recorder = delivery_recorder
        self._replay_reserver = replay_reserver
        super().__init__(
            CapabilityDefinition(
                capability_id="security-events.delivery",
                version="1.0",
            ),
            operations={
                "record_event": CapabilityOperation(
                    target=self.record_event,
                    delegated=True,
                ),
                "resolve_subscription": CapabilityOperation(
                    target=self.resolve_subscription,
                    delegated=True,
                ),
                "record_delivery": CapabilityOperation(
                    target=self.record_delivery,
                    delegated=True,
                ),
                "reserve_replay": CapabilityOperation(
                    target=self.reserve_replay,
                    delegated=True,
                ),
                "transmit": CapabilityOperation(
                    target=self.transmit,
                    delegated=True,
                ),
                "receive": CapabilityOperation(
                    target=self.receive,
                    delegated=True,
                ),
            },
        )

    async def record_event(self, event: SecurityEvent) -> object:
        return await _resolve(self._event_recorder(event))

    async def resolve_subscription(
        self,
        subscriber: str,
        event: SecurityEvent,
    ) -> SecurityEventSubscription | None:
        return await _resolve(self._subscription_resolver(subscriber, event))

    async def record_delivery(self, delivery: SecurityEventDelivery) -> object:
        return await _resolve(self._delivery_recorder(delivery))

    async def reserve_replay(self, event: SecurityEvent) -> bool:
        return bool(await _resolve(self._replay_reserver(event)))

    async def transmit(self, event: SecurityEvent, subscriber: str) -> str:
        subscription = await self.resolve_subscription(subscriber, event)
        if subscription is None:
            raise LookupError("security-event subscription is unavailable")
        if subscription.event_types and event.event_type not in subscription.event_types:
            raise PermissionError("security-event type is not subscribed")

        await self.record_event(event)
        encoded = await _resolve(self._transmitter.transmit(event, subscriber))
        await self.record_delivery(
            SecurityEventDelivery(
                event_id=event.token_id,
                subscriber=subscriber,
                attempted_at=datetime.now(timezone.utc),
                accepted=True,
            )
        )
        return encoded

    async def receive(self, encoded: str | bytes) -> SecurityEvent:
        event = await _resolve(self._receiver.receive(encoded))
        if not await self.reserve_replay(event):
            raise ValueError("security-event replay detected")
        await self.record_event(event)
        return event


__all__ = [
    "DeliveryRecorder",
    "EventRecorder",
    "ReplayReserver",
    "SecurityEventsCapability",
    "SubscriptionResolver",
]
