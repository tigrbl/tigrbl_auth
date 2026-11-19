"""Local recovery code authenticator provider."""

from __future__ import annotations

from tba_bases_authenticator import AuthenticatorBase, CredentialKindMixin, RecoveryCodeVerifierMixin
from tba_contracts_identity.authenticators import AuthenticationFactorClass, AuthenticatorKind
from tba_contracts_identity.credentials import CredentialKind


class RecoveryCodeLocalAuthenticator(RecoveryCodeVerifierMixin, CredentialKindMixin, AuthenticatorBase):
    def __init__(self) -> None:
        super().__init__(
            kind=AuthenticatorKind.RECOVERY_CODE_LOCAL,
            factor_class=AuthenticationFactorClass.KNOWLEDGE,
            credential_kind=CredentialKind.RECOVERY_CODE,
            description="Local one-time recovery code authentication.",
        )


__all__ = ["RecoveryCodeLocalAuthenticator"]
