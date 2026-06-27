"""Local API key authenticator provider."""

from __future__ import annotations

from tigrbl_identity_authenticator_bases import AuthenticatorBase, CredentialKindMixin, SecretVerifierMixin
from tigrbl_identity_contracts.authenticators import AuthenticationFactorClass, AuthenticatorKind
from tigrbl_identity_contracts.credentials import CredentialKind


class ApiKeyLocalAuthenticator(SecretVerifierMixin, CredentialKindMixin, AuthenticatorBase):
    def __init__(self) -> None:
        super().__init__(
            kind=AuthenticatorKind.API_KEY_LOCAL,
            factor_class=AuthenticationFactorClass.POSSESSION,
            credential_kind=CredentialKind.API_KEY,
            description="Local API key authentication.",
        )


__all__ = ["ApiKeyLocalAuthenticator"]
