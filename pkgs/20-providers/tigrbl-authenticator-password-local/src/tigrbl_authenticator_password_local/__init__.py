"""Local password authenticator provider."""

from __future__ import annotations

from tigrbl_identity_authenticator_bases import AmrEmitterMixin, AuthenticatorBase, CredentialKindMixin, SecretVerifierMixin
from tigrbl_identity_contracts.authenticators import AuthenticationFactorClass, AuthenticatorKind
from tigrbl_identity_contracts.credentials import CredentialKind


class PasswordLocalAuthenticator(AmrEmitterMixin, SecretVerifierMixin, CredentialKindMixin, AuthenticatorBase):
    def __init__(self, *, amr_validator=None) -> None:
        self.amr_validator = amr_validator
        super().__init__(
            kind=AuthenticatorKind.PASSWORD_LOCAL,
            factor_class=AuthenticationFactorClass.KNOWLEDGE,
            credential_kind=CredentialKind.PASSWORD,
            amr=("pwd",),
            description="Local memorized-secret password authentication.",
        )


__all__ = ["PasswordLocalAuthenticator"]
