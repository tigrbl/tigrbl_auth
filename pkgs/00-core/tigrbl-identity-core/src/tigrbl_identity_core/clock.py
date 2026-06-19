from __future__ import annotations

"""Clock primitives shared by identity packages."""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Protocol

UTC = timezone.utc


class Clock(Protocol):
    def now(self) -> datetime:
        """Return an aware UTC timestamp."""


@dataclass(frozen=True, slots=True)
class SystemClock:
    def now(self) -> datetime:
        return datetime.now(UTC)


@dataclass(frozen=True, slots=True)
class FrozenClock:
    value: datetime

    def now(self) -> datetime:
        if self.value.tzinfo is None:
            return self.value.replace(tzinfo=UTC)
        return self.value.astimezone(UTC)


def unix_seconds(clock: Clock | None = None) -> int:
    active = clock or SystemClock()
    return int(active.now().timestamp())


__all__ = ["Clock", "FrozenClock", "SystemClock", "unix_seconds"]
