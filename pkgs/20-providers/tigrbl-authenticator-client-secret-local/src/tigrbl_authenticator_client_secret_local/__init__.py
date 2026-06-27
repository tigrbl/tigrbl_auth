"""Local OAuth client secret authenticator provider."""

from __future__ import annotations

from tigrbl_identity_authenticator_bases import AuthenticatorBase, CredentialKindMixin, SecretVerifierMixin
from tigrbl_identity_contracts.authenticators import AuthenticationFactorClass, AuthenticatorKind
from tigrbl_identity_contracts.credentials import CredentialKind


class ClientSecretLocalAuthenticator(SecretVerifierMixin, CredentialKindMixin, AuthenticatorBase):
    def __init__(self) -> None:
        super().__init__(
            kind=AuthenticatorKind.CLIENT_SECRET_LOCAL,
            factor_class=AuthenticationFactorClass.SERVICE,
            credential_kind=CredentialKind.CLIENT_SECRET,
            description="Local OAuth client secret authentication.",
        )


__all__ = ["ClientSecretLocalAuthenticator"]
