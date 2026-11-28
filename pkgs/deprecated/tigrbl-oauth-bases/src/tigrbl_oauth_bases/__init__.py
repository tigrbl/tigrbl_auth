"""Deprecated facade for protocol-neutral authorization bases."""

import warnings

from tigrbl_authz_policy_bases import ScopeMatcherBase
from tigrbl_token_bases import (
    DelegationActorChainValidatorBase,
    ProfiledTokenVerifierBase,
    RichAuthorizationDetailValidatorBase,
    StepUpAuthenticationEvaluatorBase,
)

warnings.warn(
    "tigrbl_oauth_bases is deprecated; use the neutral base packages",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = [
    "DelegationActorChainValidatorBase",
    "ProfiledTokenVerifierBase",
    "RichAuthorizationDetailValidatorBase",
    "ScopeMatcherBase",
    "StepUpAuthenticationEvaluatorBase",
]
