"""Compatibility exports for protocol-neutral identity bases."""

from tigrbl_identity_claims_bases import ClaimsProviderBase
from tigrbl_identity_model_bases import SubjectIdentifierStrategyBase
from tigrbl_authentication_assurance_bases import (
    AuthenticationContextEvaluatorBase,
    IdentityAssuranceClaimsProviderBase,
    VerifiedClaimsValidatorBase,
)

EapAcrEvaluatorBase = AuthenticationContextEvaluatorBase

__all__ = [
    "ClaimsProviderBase",
    "EapAcrEvaluatorBase",
    "IdentityAssuranceClaimsProviderBase",
    "SubjectIdentifierStrategyBase",
    "VerifiedClaimsValidatorBase",
]
