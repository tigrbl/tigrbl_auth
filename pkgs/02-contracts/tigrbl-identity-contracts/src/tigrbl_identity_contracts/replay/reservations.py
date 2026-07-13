"""Protocol-neutral replay reservation contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Mapping, Protocol


@dataclass(frozen=True, slots=True)
class ReplayKey:
    namespace: str
    value: str
    tenant_id: str | None = None
    issuer: str | None = None

    def __post_init__(self) -> None:
        if not self.namespace.strip() or not self.value:
            raise ValueError("replay namespace and key value are required")


@dataclass(frozen=True, slots=True)
class ReplayReservationRequest:
    key: ReplayKey
    expires_at: datetime
    context: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.expires_at.tzinfo is None:
            raise ValueError("replay reservation expiry must be timezone-aware")
        object.__setattr__(self, "context", dict(self.context))


@dataclass(frozen=True, slots=True)
class ReplayReservationResult:
    accepted: bool
    key_digest: str
    expires_at: datetime
    duplicate: bool = False
    provider_id: str = ""


class ReplayReservationPort(Protocol):
    async def check_and_reserve(
        self, request: ReplayReservationRequest, /
    ) -> ReplayReservationResult: ...


__all__ = [
    "ReplayKey",
    "ReplayReservationPort",
    "ReplayReservationRequest",
    "ReplayReservationResult",
]
