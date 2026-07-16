from dataclasses import dataclass, field
from typing import Mapping, Sequence

from .constraints import IssuerTrustResult, ReplayValidation, SenderConstraint
from .profiles import TokenProfile


@dataclass(frozen=True, slots=True)
class TokenVerificationRequest:
    token: str | bytes
    expected_profile: TokenProfile
    expected_issuer: str | None = None
    expected_audience: str | None = None
    sender_constraint: SenderConstraint | None = None


@dataclass(frozen=True, slots=True)
class TokenVerificationResult:
    valid: bool
    profile: TokenProfile
    claims: Mapping[str | int, object] = field(default_factory=dict)
    errors: Sequence[str] = ()
    issuer_trust: IssuerTrustResult | None = None
    replay: ReplayValidation | None = None


@dataclass(frozen=True, slots=True)
class TokenIntrospectionRequest:
    token: str
    expected_profile: TokenProfile | None = None

    def __post_init__(self) -> None:
        if not self.token:
            raise ValueError("token is required for introspection")


@dataclass(frozen=True, slots=True)
class TokenIntrospectionResult:
    active: bool
    claims: Mapping[str, object] = field(default_factory=dict)
    profile: TokenProfile | None = None
    reason: str | None = None


__all__ = [
    "TokenIntrospectionRequest",
    "TokenIntrospectionResult",
    "TokenVerificationRequest",
    "TokenVerificationResult",
]
