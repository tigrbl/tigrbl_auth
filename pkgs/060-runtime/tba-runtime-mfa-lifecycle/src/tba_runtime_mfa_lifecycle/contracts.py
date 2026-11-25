"""Factor lifecycle proof, policy, and atomic storage interfaces."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Protocol


class CeremonyKind(str, Enum):
    ENROLLMENT = "enrollment"
    STEP_UP = "step_up"


class LifecycleStatus(str, Enum):
    COMPLETED = "completed"
    CHALLENGE_REQUIRED = "challenge_required"
    REJECTED = "rejected"
    EXPIRED = "expired"


@dataclass(frozen=True, slots=True)
class FactorBinding:
    scope: str
    subject: str
    factor: str
    purpose: str

    def __post_init__(self) -> None:
        if not all((self.scope, self.subject, self.factor, self.purpose)):
            raise ValueError("scope, subject, factor and purpose are required")


@dataclass(frozen=True, slots=True)
class FactorAttempt:
    attempt_id: str
    binding: FactorBinding
    kind: CeremonyKind
    issued_at: datetime
    expires_at: datetime
    challenge: bytes = field(repr=False)
    credential_reference: str | None = field(default=None, repr=False)
    replace_reference: str | None = field(default=None, repr=False)


@dataclass(frozen=True, slots=True)
class VerifiedFactor:
    """Verified factor data from a trusted authenticator adapter.

    Use a stable replay key for the proof independent of the attempt when the
    factor can produce the same proof across attempts, such as a TOTP time step.
    """

    method: str
    replay_key: str = field(repr=False)
    credential: object = field(default=None, repr=False)


@dataclass(frozen=True, slots=True)
class FactorAssurance:
    binding: FactorBinding
    method: str
    verified_at: datetime


@dataclass(frozen=True, slots=True)
class LifecycleResult:
    status: LifecycleStatus
    attempt: FactorAttempt | None = None
    assurance: FactorAssurance | None = None


@dataclass(frozen=True, slots=True)
class AssuranceRequirement:
    required_methods: frozenset[str]
    max_age: timedelta

    def __post_init__(self) -> None:
        object.__setattr__(self, "required_methods", frozenset(self.required_methods))
        if not self.required_methods or self.max_age <= timedelta(0):
            raise ValueError(
                "assurance requires methods and a positive freshness interval"
            )


class FactorVerifier(Protocol):
    def __call__(
        self, attempt: FactorAttempt, proof: object, now: datetime, /
    ) -> VerifiedFactor | None:
        """Verify a proof using the attempt's exact binding and trusted factor policy."""


class FactorStore(Protocol):
    """Atomic storage port for the host's existing credentials and replay records."""

    def create(self, attempt: FactorAttempt, /) -> None:
        """Insert an immutable pending attempt without replacing an existing ID."""

    def get(self, attempt_id: str, /) -> FactorAttempt | None:
        """Read a pending attempt without consuming it."""

    def commit(
        self, attempt: FactorAttempt, proof: VerifiedFactor, /, *, now: datetime
    ) -> bool:
        """Commit the verified proof exactly once.

        In one transaction compare the unchanged pending attempt, check expiration
        and replacement or active credential state, record replay state, consume the
        attempt, and activate or update the credential. Roll back everything if any
        check fails. Scope replay uniqueness by account, scope, and factor.
        Never remove the old credential unless replacement commits.
        """

    def cancel(self, attempt: FactorAttempt, /) -> bool:
        """Cancel this unchanged pending attempt without modifying active credentials."""
