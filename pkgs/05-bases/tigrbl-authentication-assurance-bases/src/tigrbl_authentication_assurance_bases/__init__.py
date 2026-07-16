from abc import ABC

from tigrbl_identity_assurance_bases import (
    IdentityAssuranceClaimsProviderBase,
    VerifiedClaimsValidatorBase,
)
from tigrbl_identity_contracts.oidc.eap_acr import (
    EapAcrEvaluationRequest,
    EapAcrEvaluationResult,
    EapAcrEvaluatorPort,
)


class AuthenticationContextEvaluatorBase(EapAcrEvaluatorPort, ABC):
    def evaluate(self, request: EapAcrEvaluationRequest, /) -> EapAcrEvaluationResult:
        raise NotImplementedError


__all__ = [
    "AuthenticationContextEvaluatorBase",
    "IdentityAssuranceClaimsProviderBase",
    "VerifiedClaimsValidatorBase",
]
