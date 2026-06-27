"""Local WebAuthn authenticator provider."""

from __future__ import annotations

from tigrbl_identity_authenticator_bases import AmrEmitterMixin, ChallengeAuthenticatorBase, ChallengeLifecycleMixin, CredentialKindMixin, PhishingResistanceMixin, UserPresenceMixin, UserVerificationMixin, VerifierNameBindingMixin, WebAuthnAssertionMixin
from tigrbl_identity_contracts.authenticators import AuthenticationFactorClass, AuthenticatorKind, AuthenticatorProperty
from tigrbl_identity_contracts.credentials import CredentialKind


class WebAuthnLocalAuthenticator(
    AmrEmitterMixin,
    WebAuthnAssertionMixin,
    ChallengeLifecycleMixin,
    PhishingResistanceMixin,
    VerifierNameBindingMixin,
    UserPresenceMixin,
    UserVerificationMixin,
    CredentialKindMixin,
    ChallengeAuthenticatorBase,
):
    def __init__(self, *, amr_validator=None, amr=("hwk", "user")) -> None:
        self.amr_validator = amr_validator
        super().__init__(
            kind=AuthenticatorKind.WEBAUTHN_LOCAL,
            factor_class=AuthenticationFactorClass.POSSESSION,
            credential_kind=CredentialKind.PASSKEY_WEBAUTHN,
            amr=tuple(amr),
            properties=(
                AuthenticatorProperty.PHISHING_RESISTANT,
                AuthenticatorProperty.VERIFIER_NAME_BOUND,
                AuthenticatorProperty.USER_PRESENT,
                AuthenticatorProperty.USER_VERIFIED,
                AuthenticatorProperty.REPLAY_RESISTANT,
            ),
            description="Local WebAuthn assertion authentication.",
        )


__all__ = ["WebAuthnLocalAuthenticator"]
