"""Local OTP authenticator provider."""

from __future__ import annotations

from tba_bases_authenticator import AmrEmitterMixin, ChallengeAuthenticatorBase, ChallengeLifecycleMixin, CredentialKindMixin, OtpVerifierMixin
from tba_contracts_identity.authenticators import AuthenticationFactorClass, AuthenticatorKind
from tba_contracts_identity.credentials import CredentialKind


class OtpLocalAuthenticator(AmrEmitterMixin, OtpVerifierMixin, ChallengeLifecycleMixin, CredentialKindMixin, ChallengeAuthenticatorBase):
    def __init__(self, *, amr_validator=None) -> None:
        self.amr_validator = amr_validator
        super().__init__(
            kind=AuthenticatorKind.OTP_LOCAL,
            factor_class=AuthenticationFactorClass.POSSESSION,
            credential_kind=CredentialKind.MFA_FACTOR,
            amr=("otp",),
            description="Local one-time password authentication.",
        )


__all__ = ["OtpLocalAuthenticator"]
