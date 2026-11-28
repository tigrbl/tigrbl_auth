"""Local OAuth client secret authenticator provider."""

from __future__ import annotations

from tba_bases_authenticator import AuthenticatorBase, CredentialKindMixin, SecretVerifierMixin
from tba_contracts_identity.authenticators import AuthenticationFactorClass, AuthenticatorKind
from tba_contracts_identity.credentials import CredentialKind
from tba_contracts_identity.shared_secrets import SecretVerificationPort
from tba_provider_secret_hashing_bcrypt import BcryptSecretHasher


class ClientSecretLocalAuthenticator(SecretVerifierMixin, CredentialKindMixin, AuthenticatorBase):
    def __init__(self, *, secret_verifier: SecretVerificationPort | None = None) -> None:
        self.secret_verifier = secret_verifier or BcryptSecretHasher()
        super().__init__(
            kind=AuthenticatorKind.CLIENT_SECRET_LOCAL,
            factor_class=AuthenticationFactorClass.SERVICE,
            credential_kind=CredentialKind.CLIENT_SECRET,
            description="Local client shared-secret authentication.",
        )


__all__ = ["ClientSecretLocalAuthenticator"]
