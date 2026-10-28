"""Local password authenticator provider."""

from __future__ import annotations

from tba_bases_authenticator import AmrEmitterMixin, AuthenticatorBase, CredentialKindMixin, SecretVerifierMixin
from tba_contracts_identity.authenticators import AuthenticationFactorClass, AuthenticatorKind
from tba_contracts_identity.credentials import CredentialKind
from tba_contracts_identity.shared_secrets import SecretVerificationPort
from tba_provider_secret_hashing_bcrypt import BcryptSecretHasher


class PasswordLocalAuthenticator(AmrEmitterMixin, SecretVerifierMixin, CredentialKindMixin, AuthenticatorBase):
    def __init__(
        self,
        *,
        secret_verifier: SecretVerificationPort | None = None,
        amr_validator=None,
    ) -> None:
        self.secret_verifier = secret_verifier or BcryptSecretHasher()
        self.amr_validator = amr_validator
        super().__init__(
            kind=AuthenticatorKind.PASSWORD_LOCAL,
            factor_class=AuthenticationFactorClass.KNOWLEDGE,
            credential_kind=CredentialKind.PASSWORD,
            amr=("pwd",),
            description="Local memorized-secret password authentication.",
        )


__all__ = ["PasswordLocalAuthenticator"]
