"""Provider-side authorization continuation contracts."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Protocol


@dataclass(frozen=True, slots=True)
class ValidatedAuthorizationRequest:
    """A snapshot from the provider's authorization validation boundary."""

    issuer: str
    tenant_id: str
    client_id: str
    redirect_uri: str
    parameters: tuple[tuple[str, str], ...] = field(repr=False)

    def __post_init__(self) -> None:
        parameters = tuple((key, value) for key, value in self.parameters)
        if any(key in {"client_id", "redirect_uri"} for key, _ in parameters):
            raise ValueError("Client and redirect URI belong in the bound fields")
        object.__setattr__(self, "parameters", parameters)


@dataclass(frozen=True, slots=True)
class PendingContinuation:
    flow_id: str = field(repr=False)
    request: ValidatedAuthorizationRequest
    browser_binding: str = field(repr=False)
    started_at: datetime
    expires_at: datetime
    recover_until: datetime
    required_assurance: str | None


class ContinuationRepository(Protocol):
    """Keep a unique immutable record per flow until consumed or pruned."""

    def insert(self, continuation: PendingContinuation) -> None:
        """Insert a new record. Reject replacement of an existing flow ID."""
        ...

    def get_pending(self, flow_id: str) -> PendingContinuation | None:
        """Return a pending record, including an expired record until pruning."""
        ...

    def consume_pending(self, continuation: PendingContinuation, *, now: datetime) -> bool:
        """Atomically consume this exact pending record before its expiry."""
        ...


@dataclass(frozen=True, slots=True)
class Resume:
    request: ValidatedAuthorizationRequest


@dataclass(frozen=True, slots=True)
class Restart:
    """Identify a client for the provider's registered start routing."""

    client_id: str


@dataclass(frozen=True, slots=True)
class StayLocal:
    """Keep the browser on a provider-controlled surface."""


ContinuationOutcome = Resume | Restart | StayLocal
