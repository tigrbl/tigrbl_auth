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


@dataclass(frozen=True, slots=True)
class ReplayStoreDescriptor:
    provider_id: str
    persistence: str
    atomic_reservation: bool
    namespaces: tuple[str, ...]
    tenant_isolation: str
    expiry: str
    retention: str
    purge: str
    audit: str
    availability: str


class ReplayReservationPort(Protocol):
    async def check_and_reserve(
        self, request: ReplayReservationRequest, /
    ) -> ReplayReservationResult: ...


class ReplayCheckPort(Protocol):
    """Synchronous atomic replay boundary for synchronous protocol decoders."""

    def check_and_store(self, key: str, *, now: int | None = None, ttl_s: int) -> bool: ...
    def snapshot(self) -> Mapping[str, int]: ...
    def clear(self) -> None: ...


class SingleUseNoncePort(Protocol):
    """Synchronous single-use nonce boundary."""

    def issue(self, *, ttl_s: int) -> str: ...
    def register(self, nonce: str, *, ttl_s: int) -> str: ...
    def consume(self, nonce: str, *, now: int | None = None) -> bool: ...
    def snapshot(self) -> Mapping[str, object]: ...
    def clear(self) -> None: ...


__all__ = [
    "ReplayKey",
    "ReplayCheckPort",
    "ReplayReservationPort",
    "ReplayReservationRequest",
    "ReplayReservationResult",
    "ReplayStoreDescriptor",
    "SingleUseNoncePort",
]
