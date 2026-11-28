from abc import ABC

from tba_bases_identity_assurance import (
    IdentityAssuranceClaimsProviderBase,
    VerifiedClaimsValidatorBase,
)
from tba_contracts_identity.oidc.eap_acr import (
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
