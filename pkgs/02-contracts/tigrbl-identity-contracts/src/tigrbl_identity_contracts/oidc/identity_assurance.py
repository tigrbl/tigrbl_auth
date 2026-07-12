from dataclasses import dataclass, field
from typing import Mapping, Protocol, Sequence

from ..assurance import VerifiedClaims, VerifiedClaimsRequest


@dataclass(frozen=True, slots=True)
class IdentityAssuranceRequest:
    verified_claims: VerifiedClaimsRequest
    purpose: str | None = None
    max_age: int | None = None


@dataclass(frozen=True, slots=True)
class IdentityAssuranceResult:
    verified_claims: VerifiedClaims | None
    satisfied: bool
    errors: Sequence[str] = ()
    metadata: Mapping[str, object] = field(default_factory=dict)


class IdentityAssuranceClaimsProviderPort(Protocol):
    def provide(
        self, subject: str, request: IdentityAssuranceRequest, /
    ) -> IdentityAssuranceResult: ...


class VerifiedClaimsValidatorPort(Protocol):
    def validate(
        self, verified_claims: VerifiedClaims, /
    ) -> IdentityAssuranceResult: ...


__all__ = [
    "IdentityAssuranceClaimsProviderPort",
    "IdentityAssuranceRequest",
    "IdentityAssuranceResult",
    "VerifiedClaimsValidatorPort",
]
