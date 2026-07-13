from abc import ABC
from typing import Mapping

from tigrbl_identity_contracts.tokens import (
    TokenIssuerPort,
    ProtectedTokenEnvelope,
    TokenProfile,
    TokenVerificationRequest,
    TokenVerificationResult,
    TokenVerifierPort,
    VerifiedTokenEnvelope,
)


class ProfiledTokenIssuerBase(TokenIssuerPort, ABC):
    def issue(
        self, profile: TokenProfile, claims: Mapping[str | int, object], /
    ) -> str | bytes:
        raise NotImplementedError


class ProfiledTokenVerifierBase(TokenVerifierPort, ABC):
    def verify(self, request: TokenVerificationRequest, /) -> TokenVerificationResult:
        raise NotImplementedError


class TokenEnvelopeVerifierBase(ABC):
    """Verify a cryptographic envelope without making an appraisal decision."""

    def verify_envelope(
        self, envelope: ProtectedTokenEnvelope, /
    ) -> VerifiedTokenEnvelope:
        raise NotImplementedError


class EatTokenEnvelopeVerifierBase(TokenEnvelopeVerifierBase):
    """Envelope verifier constrained to the EAT token profile."""


class RichAuthorizationDetailValidatorBase(ABC):
    def validate_authorization_details(self, details: object, /) -> bool:
        raise NotImplementedError


class DelegationActorChainValidatorBase(ABC):
    def validate_actor_chain(self, chain: object, /) -> bool:
        raise NotImplementedError


class StepUpAuthenticationEvaluatorBase(ABC):
    def requires_step_up(self, context: object, /) -> bool:
        raise NotImplementedError


__all__ = [
    "DelegationActorChainValidatorBase",
    "ProfiledTokenIssuerBase",
    "ProfiledTokenVerifierBase",
    "RichAuthorizationDetailValidatorBase",
    "StepUpAuthenticationEvaluatorBase",
    "EatTokenEnvelopeVerifierBase",
    "TokenEnvelopeVerifierBase",
]
