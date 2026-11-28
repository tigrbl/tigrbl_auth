"""Contracts for continuing an already-validated hosted authorization request."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Protocol


def require_aware(value: datetime) -> None:
    if value.utcoffset() is None:
        raise ValueError("authorization continuation timestamps must be timezone-aware")


@dataclass(frozen=True, slots=True)
class ValidatedAuthorizationRequest:
    """Snapshot of the request as validated by the host authorization endpoint."""

    issuer: str
    client_id: str
    redirect_uri: str
    parameters: tuple[tuple[str, str], ...] = field(repr=False)
    tenant_id: str | None = None

    def __post_init__(self) -> None:
        if not self.issuer or not self.client_id or not self.redirect_uri:
            raise ValueError("issuer, client_id and redirect_uri are required")
        if self.tenant_id == "":
            raise ValueError("tenant ID must be nonempty when supplied")
        snapshot = tuple((key, value) for key, value in self.parameters)
        if any(
            not isinstance(key, str) or not isinstance(value, str)
            for key, value in snapshot
        ):
            raise ValueError("validated request parameters must be strings")
        parameters = dict(snapshot)
        if len(parameters) != len(snapshot):
            raise ValueError("validated request contains duplicate parameters")
        if (
            parameters.get("client_id") != self.client_id
            or parameters.get("redirect_uri") != self.redirect_uri
        ):
            raise ValueError(
                "validated request disagrees with its client or redirect URI"
            )
        object.__setattr__(self, "parameters", snapshot)

    @classmethod
    def from_parameters(
        cls, issuer: str, parameters: Mapping[str, str], *, tenant_id: str | None = None
    ) -> ValidatedAuthorizationRequest:
        return cls(
            issuer,
            parameters.get("client_id", ""),
            parameters.get("redirect_uri", ""),
            tuple(parameters.items()),
            tenant_id=tenant_id,
        )


@dataclass(frozen=True, slots=True)
class ContinuationRequirements:
    required_methods: frozenset[str] = frozenset()
    not_before: datetime | None = None
    subject: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "required_methods", frozenset(self.required_methods))
        if self.not_before is not None:
            require_aware(self.not_before)


@dataclass(frozen=True, slots=True)
class AuthenticationEvidence:
    """Trusted host authentication evidence for this browser transaction."""

    subject: str
    authenticated_at: datetime
    methods: frozenset[str]

    def __post_init__(self) -> None:
        require_aware(self.authenticated_at)
        object.__setattr__(self, "methods", frozenset(self.methods))


@dataclass(frozen=True, slots=True)
class ContinuationRecord:
    flow_id: str
    browser_digest: bytes = field(repr=False)
    request: ValidatedAuthorizationRequest
    requirements: ContinuationRequirements
    issued_at: datetime
    expires_at: datetime


class ContinuationStatus(str, Enum):
    RESUME = "resume"
    RESTART_REQUIRED = "restart_required"
    UNAVAILABLE = "unavailable"


class ContinuationReason(str, Enum):
    INVALID_FLOW = "invalid_flow"
    AUTHENTICATION_REQUIRED = "authentication_required"
    REGISTRATION_CHANGED = "registration_changed"
    STORAGE_UNAVAILABLE = "storage_unavailable"


@dataclass(frozen=True, slots=True)
class ContinuationResult:
    status: ContinuationStatus
    request: ValidatedAuthorizationRequest | None = None
    reason: ContinuationReason | None = None
    restart_client_id: str | None = None


class ContinuationUnavailable(RuntimeError):
    """Expected host storage or registration service unavailability."""


class ContinuationStore(Protocol):
    """Storage for immutable records. Map backend unavailability to ContinuationUnavailable."""

    def create(self, record: ContinuationRecord, /) -> None:
        """Insert a new record, rejecting duplicate flow IDs."""

    def get(self, flow_id: str, /) -> ContinuationRecord | None:
        """Return an unconsumed record, including expired records retained for recovery."""

    def consume(self, record: ContinuationRecord, /, *, now: datetime) -> bool:
        """Atomically consume the matching unexpired record once.

        Return False if absent, changed, expired or already consumed. Never
        replace or recreate an existing flow ID.
        """
