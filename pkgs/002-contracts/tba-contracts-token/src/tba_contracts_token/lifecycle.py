from dataclasses import dataclass, field
from datetime import timedelta
from typing import Final, Mapping, Sequence

DEFAULT_ACCESS_TOKEN_TTL: Final[timedelta] = timedelta(minutes=60)
DEFAULT_REFRESH_TOKEN_TTL: Final[timedelta] = timedelta(days=7)


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
        if not all((self.subject, self.tenant_id, self.client_id, self.issuer)):
            raise ValueError("subject, tenant_id, client_id, and issuer are required")


@dataclass(frozen=True, slots=True)
class RefreshTokenRedemptionRequest:
    refresh_token: str
    tenant_id: str
    client_id: str
    certificate_thumbprint: str | None = None
    requested_audience: str | None = None
    token_type: str = "bearer"

    def __post_init__(self) -> None:
        if not all((self.refresh_token, self.tenant_id, self.client_id)):
            raise ValueError("refresh_token, tenant_id, and client_id are required")


@dataclass(frozen=True, slots=True)
class IssuedTokenPair:
    access_token: str
    refresh_token: str | None
    token_type: str = "bearer"

    def __post_init__(self) -> None:
        if not self.access_token:
            raise ValueError("access_token is required")


__all__ = [
    "DEFAULT_ACCESS_TOKEN_TTL",
    "DEFAULT_REFRESH_TOKEN_TTL",
    "IssuedTokenPair",
    "RefreshTokenRedemptionRequest",
    "TokenPairIssueRequest",
    "TokenRevocationRequest",
    "TokenRevocationResult",
]
