"""Local recovery code authenticator provider."""

from __future__ import annotations

from tigrbl_authenticator_bases import AuthenticatorBase, CredentialKindMixin, RecoveryCodeVerifierMixin
from tigrbl_identity_contracts.authenticators import AuthenticationFactorClass, AuthenticatorKind
from tigrbl_identity_contracts.credentials import CredentialKind


class RecoveryCodeLocalAuthenticator(RecoveryCodeVerifierMixin, CredentialKindMixin, AuthenticatorBase):
    def __init__(self) -> None:
        super().__init__(
            kind=AuthenticatorKind.RECOVERY_CODE_LOCAL,
            factor_class=AuthenticationFactorClass.KNOWLEDGE,
            credential_kind=CredentialKind.RECOVERY_CODE,
            description="Local one-time recovery code authentication.",
        )


__all__ = ["RecoveryCodeLocalAuthenticator"]
