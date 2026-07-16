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


class EapAcrEvaluatorBase(EapAcrEvaluatorPort, ABC):
    def evaluate(self, request: EapAcrEvaluationRequest, /) -> EapAcrEvaluationResult:
        raise NotImplementedError


__all__ = [
    "EapAcrEvaluatorBase",
    "IdentityAssuranceClaimsProviderBase",
    "VerifiedClaimsValidatorBase",
]

AuthenticationContextEvaluatorBase = EapAcrEvaluatorBase
__all__.append("AuthenticationContextEvaluatorBase")
