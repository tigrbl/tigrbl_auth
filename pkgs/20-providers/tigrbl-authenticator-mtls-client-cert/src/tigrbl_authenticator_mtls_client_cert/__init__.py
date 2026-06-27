"""mTLS client certificate authenticator provider."""

from __future__ import annotations

from tigrbl_identity_authenticator_bases import AuthenticatorBase, CredentialKindMixin, SenderConstraintMixin
from tigrbl_identity_contracts.authenticators import AuthenticationFactorClass, AuthenticatorKind, AuthenticatorProperty
from tigrbl_identity_contracts.credentials import CredentialKind


class MtlsClientCertAuthenticator(SenderConstraintMixin, CredentialKindMixin, AuthenticatorBase):
    def __init__(self) -> None:
        super().__init__(
            kind=AuthenticatorKind.MTLS_CLIENT_CERT,
            factor_class=AuthenticationFactorClass.POSSESSION,
            credential_kind=CredentialKind.MTLS_CERTIFICATE,
            properties=(
                AuthenticatorProperty.SENDER_CONSTRAINED,
                AuthenticatorProperty.REPLAY_RESISTANT,
            ),
            description="mTLS client certificate proof authentication.",
        )


__all__ = ["MtlsClientCertAuthenticator"]
