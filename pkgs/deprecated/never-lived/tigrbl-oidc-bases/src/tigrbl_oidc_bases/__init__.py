"""Deprecated facade for neutral identity and assurance bases."""

import warnings

from tigrbl_authentication_assurance_bases import (
    AuthenticationContextEvaluatorBase,
    IdentityAssuranceClaimsProviderBase,
    VerifiedClaimsValidatorBase,
)
from tigrbl_identity_claims_bases import ClaimsProviderBase
from tigrbl_identity_model_bases import SubjectIdentifierStrategyBase

warnings.warn(
    "tigrbl_oidc_bases is deprecated; use the neutral base packages",
    DeprecationWarning,
    stacklevel=2,
)

EapAcrEvaluatorBase = AuthenticationContextEvaluatorBase

__all__ = [
    "ClaimsProviderBase",
    "EapAcrEvaluatorBase",
    "IdentityAssuranceClaimsProviderBase",
    "SubjectIdentifierStrategyBase",
    "VerifiedClaimsValidatorBase",
]
