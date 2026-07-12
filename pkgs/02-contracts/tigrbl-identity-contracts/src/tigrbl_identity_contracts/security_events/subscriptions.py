from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class SecurityEventSubscription:
    subscriber: str
    event_types: tuple[str, ...]
    delivery_method: str


@dataclass(frozen=True, slots=True)
class SecurityEventDelivery:
    event_id: str
    subscriber: str
    attempted_at: datetime
    accepted: bool
    response_code: int | None = None


__all__ = ["SecurityEventDelivery", "SecurityEventSubscription"]
