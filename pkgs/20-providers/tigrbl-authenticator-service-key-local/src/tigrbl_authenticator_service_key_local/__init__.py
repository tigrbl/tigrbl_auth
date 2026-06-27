"""Local service key authenticator provider."""

from __future__ import annotations

from tigrbl_identity_authenticator_bases import AuthenticatorBase, CredentialKindMixin, SecretVerifierMixin
from tigrbl_identity_contracts.authenticators import AuthenticationFactorClass, AuthenticatorKind
from tigrbl_identity_contracts.credentials import CredentialKind


class ServiceKeyLocalAuthenticator(SecretVerifierMixin, CredentialKindMixin, AuthenticatorBase):
    def __init__(self) -> None:
        super().__init__(
            kind=AuthenticatorKind.SERVICE_KEY_LOCAL,
            factor_class=AuthenticationFactorClass.SERVICE,
            credential_kind=CredentialKind.SERVICE_KEY,
            description="Local service key authentication.",
        )


__all__ = ["ServiceKeyLocalAuthenticator"]
