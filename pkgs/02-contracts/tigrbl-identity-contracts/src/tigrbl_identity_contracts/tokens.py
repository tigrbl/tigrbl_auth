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


@dataclass(frozen=True, slots=True)
class TokenRevocationRequest:
    token: str
    token_type_hint: str | None = None
    reason: str = "revoked"

    def __post_init__(self) -> None:
        if not self.token:
            raise ValueError("token is required for revocation")


@dataclass(frozen=True, slots=True)
class TokenRevocationResult:
    revoked: bool = True
    token_reference: str | None = None


@dataclass(frozen=True, slots=True)
class TokenPairIssueRequest:
    """Normalized input for issuing and durably recording an OAuth token pair."""

    subject: str
    tenant_id: str
    client_id: str
    issuer: str
    scope: str | None = None
    audience: str | Sequence[str] | None = None
    certificate_thumbprint: str | None = None
    confirmation: Mapping[str, object] | None = None
    refresh_family_id: str | None = None
    refresh_parent_token: str | None = None
    token_type: str = "bearer"
    extra_claims: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.subject:
            raise ValueError("token subject is required")
        if not self.tenant_id:
            raise ValueError("token tenant_id is required")
        if not self.client_id:
            raise ValueError("token client_id is required")
        if not self.issuer:
            raise ValueError("token issuer is required")


@dataclass(frozen=True, slots=True)
class RefreshTokenRedemptionRequest:
    """Ephemeral input for rotating one client-bound refresh token."""

    refresh_token: str
    tenant_id: str
    client_id: str
    certificate_thumbprint: str | None = None
    requested_audience: str | None = None
    token_type: str = "bearer"

    def __post_init__(self) -> None:
        if not self.refresh_token:
            raise ValueError("refresh_token is required")
        if not self.tenant_id:
            raise ValueError("tenant_id is required")
        if not self.client_id:
            raise ValueError("client_id is required")


@dataclass(frozen=True, slots=True)
class IssuedTokenPair:
    access_token: str
    refresh_token: str | None
    token_type: str = "bearer"

    def __post_init__(self) -> None:
        if not self.access_token:
            raise ValueError("access_token is required")


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
    "IssuedTokenPair",
    "InvalidRefreshTokenError",
    "RefreshTokenError",
    "RefreshTokenReuseError",
    "ReplayValidation",
    "RefreshTokenRedemptionRequest",
    "SenderConstraint",
    "TokenIssuerPort",
    "TokenIntrospectionRequest",
    "TokenIntrospectionResult",
    "TokenPairIssueRequest",
    "TokenRevocationRequest",
    "TokenRevocationResult",
    "TokenEnvelopeFormat",
    "TokenProfile",
    "ProtectedTokenEnvelope",
    "TokenVerificationRequest",
    "TokenVerificationResult",
    "TokenVerifierPort",
    "VerifiedTokenEnvelope",
]
