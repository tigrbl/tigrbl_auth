"""Local OAuth client secret authenticator provider."""

from __future__ import annotations

from tigrbl_authenticator_bases import AuthenticatorBase, CredentialKindMixin, SecretVerifierMixin
from tigrbl_identity_contracts.authenticators import AuthenticationFactorClass, AuthenticatorKind
from tigrbl_identity_contracts.credentials import CredentialKind
from tigrbl_identity_contracts.shared_secrets import SecretVerificationPort
from tigrbl_secret_hashing_bcrypt_provider import BcryptSecretHasher


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
