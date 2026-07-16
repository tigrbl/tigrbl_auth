from abc import ABC

from tigrbl_identity_assurance_contracts import (
    IdentityAssuranceClaimsProviderPort,
    IdentityAssuranceRequest,
    IdentityAssuranceResult,
    VerifiedClaims,
    VerifiedClaimsValidatorPort,
)


class IdentityAssuranceClaimsProviderBase(IdentityAssuranceClaimsProviderPort, ABC):
    def provide(
        self, subject: str, request: IdentityAssuranceRequest, /
    ) -> IdentityAssuranceResult:
        raise NotImplementedError


class VerifiedClaimsValidatorBase(VerifiedClaimsValidatorPort, ABC):
    def validate(self, verified_claims: VerifiedClaims, /) -> IdentityAssuranceResult:
        raise NotImplementedError


class AssuranceEvidenceEvaluatorBase(ABC):
    def evaluate_evidence(self, evidence: object, /) -> object:
        raise NotImplementedError


__all__ = [
    "AssuranceEvidenceEvaluatorBase",
    "IdentityAssuranceClaimsProviderBase",
    "VerifiedClaimsValidatorBase",
]
