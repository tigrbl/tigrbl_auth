"""Security-event table aliases and executable runtime specifications."""

from tigrbl_identity_storage.tables import (
    SecurityEvent,
    SecurityEventDelivery,
    SecurityEventReplay,
    SecurityEventSubscription,
)

from ..derive import deriveRuntimeTableSpec
from ..make import makeRuntimeOperation
from ..ops.security_events import (
    enqueue_security_event_delivery,
    record_security_event,
    record_security_event_subscription,
    reserve_security_event_replay,
)

SecurityEventTable = SecurityEvent
SecurityEventDeliveryTable = SecurityEventDelivery
SecurityEventReplayTable = SecurityEventReplay
SecurityEventSubscriptionTable = SecurityEventSubscription

SecurityEventRuntimeSpec = deriveRuntimeTableSpec(
    SecurityEventTable,
    operations=(
        makeRuntimeOperation(alias="record_event", handler=record_security_event),
    ),
)
SecurityEventDeliveryRuntimeSpec = deriveRuntimeTableSpec(
    SecurityEventDeliveryTable,
    operations=(
        makeRuntimeOperation(
            alias="enqueue_delivery", handler=enqueue_security_event_delivery
        ),
    ),
)
SecurityEventSubscriptionRuntimeSpec = deriveRuntimeTableSpec(
    SecurityEventSubscriptionTable,
    operations=(
        makeRuntimeOperation(
            alias="record_subscription",
            handler=record_security_event_subscription,
        ),
    ),
)
SecurityEventReplayRuntimeSpec = deriveRuntimeTableSpec(
    SecurityEventReplayTable,
    operations=(
        makeRuntimeOperation(
            alias="reserve_replay", handler=reserve_security_event_replay
        ),
    ),
)

__all__ = [
    "SecurityEventDeliveryRuntimeSpec",
    "SecurityEventDeliveryTable",
    "SecurityEventReplayRuntimeSpec",
    "SecurityEventReplayTable",
    "SecurityEventRuntimeSpec",
    "SecurityEventTable",
    "SecurityEventSubscriptionRuntimeSpec",
    "SecurityEventSubscriptionTable",
]
