"""DPoP proof authenticator provider."""

from __future__ import annotations

from tba_bases_authenticator import AuthenticatorBase, CredentialKindMixin, SenderConstraintMixin
from tba_contracts_identity.authenticators import AuthenticationFactorClass, AuthenticatorKind, AuthenticatorProperty
from tba_contracts_identity.credentials import CredentialKind


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
