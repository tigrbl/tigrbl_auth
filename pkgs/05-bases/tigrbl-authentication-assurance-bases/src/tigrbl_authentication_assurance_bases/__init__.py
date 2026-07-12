from abc import ABC

from tigrbl_identity_contracts.assurance import VerifiedClaims
from tigrbl_identity_contracts.oidc.eap_acr import (
    EapAcrEvaluationRequest,
    EapAcrEvaluationResult,
    EapAcrEvaluatorPort,
)
from tigrbl_identity_contracts.oidc.identity_assurance import (
    IdentityAssuranceClaimsProviderPort,
    IdentityAssuranceRequest,
    IdentityAssuranceResult,
    VerifiedClaimsValidatorPort,
)


class AuthenticationContextEvaluatorBase(EapAcrEvaluatorPort, ABC):
    def evaluate(self, request: EapAcrEvaluationRequest, /) -> EapAcrEvaluationResult:
        raise NotImplementedError


class IdentityAssuranceClaimsProviderBase(IdentityAssuranceClaimsProviderPort, ABC):
    def provide(
        self, subject: str, request: IdentityAssuranceRequest, /
    ) -> IdentityAssuranceResult:
        raise NotImplementedError


class VerifiedClaimsValidatorBase(VerifiedClaimsValidatorPort, ABC):
    def validate(self, verified_claims: VerifiedClaims, /) -> IdentityAssuranceResult:
        raise NotImplementedError


__all__ = [
    "AuthenticationContextEvaluatorBase",
    "IdentityAssuranceClaimsProviderBase",
    "VerifiedClaimsValidatorBase",
]
