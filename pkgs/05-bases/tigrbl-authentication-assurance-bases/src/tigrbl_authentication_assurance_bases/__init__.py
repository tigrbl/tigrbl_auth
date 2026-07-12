from abc import ABC


class AuthenticationContextEvaluatorBase(ABC):
    def evaluate_context(self, evidence: object, /) -> str:
        raise NotImplementedError


class IdentityAssuranceClaimsProviderBase(ABC):
    def verified_claims(self, subject: str, /) -> object:
        raise NotImplementedError


class VerifiedClaimsValidatorBase(ABC):
    def validate_verified_claims(self, claims: object, /) -> bool:
        raise NotImplementedError


__all__ = [
    "AuthenticationContextEvaluatorBase",
    "IdentityAssuranceClaimsProviderBase",
    "VerifiedClaimsValidatorBase",
]
