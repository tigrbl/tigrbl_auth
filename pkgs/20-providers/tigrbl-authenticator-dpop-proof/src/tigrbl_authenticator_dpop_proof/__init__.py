"""DPoP proof authenticator provider."""

from __future__ import annotations

from tigrbl_authenticator_bases import AuthenticatorBase, CredentialKindMixin, SenderConstraintMixin
from tigrbl_identity_contracts.authenticators import AuthenticationFactorClass, AuthenticatorKind, AuthenticatorProperty
from tigrbl_identity_contracts.credentials import CredentialKind


class DpopProofAuthenticator(SenderConstraintMixin, CredentialKindMixin, AuthenticatorBase):
    def __init__(self) -> None:
        super().__init__(
            kind=AuthenticatorKind.DPOP_PROOF,
            factor_class=AuthenticationFactorClass.POSSESSION,
            credential_kind=CredentialKind.DPOP_KEY,
            properties=(
                AuthenticatorProperty.SENDER_CONSTRAINED,
                AuthenticatorProperty.REPLAY_RESISTANT,
            ),
            description="DPoP proof-of-possession authentication.",
        )


__all__ = ["DpopProofAuthenticator"]
