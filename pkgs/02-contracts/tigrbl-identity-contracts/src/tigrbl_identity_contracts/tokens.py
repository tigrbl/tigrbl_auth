from __future__ import annotations

from datetime import timedelta
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Final, Mapping, Protocol, Sequence

from tigrbl_identity_core.errors import (
    InvalidRefreshTokenError,
    RefreshTokenError,
    RefreshTokenReuseError,
)

DEFAULT_ACCESS_TOKEN_TTL: Final[timedelta] = timedelta(minutes=60)
DEFAULT_REFRESH_TOKEN_TTL: Final[timedelta] = timedelta(days=7)


class TokenProfile(StrEnum):
    ACCESS_TOKEN = "access-token"
    ID_TOKEN = "id-token"
    REFRESH_TOKEN = "refresh-token"
    SECURITY_EVENT_TOKEN = "security-event-token"
    ENTITY_ATTESTATION_TOKEN = "entity-attestation-token"
    JWT_SVID = "jwt-svid"
    SD_JWT_KEY_BINDING = "kb-jwt"
    WALLET_ATTESTATION = "wallet-attestation"


class TokenEnvelopeFormat(StrEnum):
    """Cryptographic envelope used to protect a semantic token payload."""

    JWT = "jwt"
    CWT = "cwt"


@dataclass(frozen=True, slots=True)
class ProtectedTokenEnvelope:
    serialized: str | bytes
    format: TokenEnvelopeFormat
    profile: TokenProfile


@dataclass(frozen=True, slots=True)
class VerifiedTokenEnvelope:
    """Integrity-verified envelope; issuer trust and appraisal remain separate."""

    envelope: ProtectedTokenEnvelope
    claims: Mapping[str | int, object]
    key_id: str | None = None
    algorithm: str | int | None = None


@dataclass(frozen=True, slots=True)
class SenderConstraint:
    method: str
    confirmation: Mapping[str, object]


@dataclass(frozen=True, slots=True)
class ReplayValidation:
    accepted: bool
    token_id: str | None = None
    reason: str | None = None


@dataclass(frozen=True, slots=True)
class IssuerTrustResult:
    trusted: bool
    issuer: str
    reason: str | None = None


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


class TokenIssuerPort(Protocol):
    def issue(
        self, profile: TokenProfile, claims: Mapping[str | int, object], /
    ) -> str | bytes: ...


class TokenVerifierPort(Protocol):
    def verify(
        self, request: TokenVerificationRequest, /
    ) -> TokenVerificationResult: ...


__all__ = [
    "DEFAULT_ACCESS_TOKEN_TTL",
    "DEFAULT_REFRESH_TOKEN_TTL",
    "IssuerTrustResult",
    "InvalidRefreshTokenError",
    "RefreshTokenError",
    "RefreshTokenReuseError",
    "ReplayValidation",
    "SenderConstraint",
    "TokenIssuerPort",
    "TokenEnvelopeFormat",
    "TokenProfile",
    "ProtectedTokenEnvelope",
    "TokenVerificationRequest",
    "TokenVerificationResult",
    "TokenVerifierPort",
    "VerifiedTokenEnvelope",
]
