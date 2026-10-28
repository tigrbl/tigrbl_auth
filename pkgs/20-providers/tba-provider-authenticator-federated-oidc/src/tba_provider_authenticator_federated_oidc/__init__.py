"""Federated OIDC authenticator provider."""

from __future__ import annotations

from tba_bases_authenticator import AmrEmitterMixin, AuthenticatorBase
from tba_contracts_identity.authenticators import AuthenticationFactorClass, AuthenticatorKind


class FederatedOidcAuthenticator(AmrEmitterMixin, AuthenticatorBase):
    def __init__(self, *, amr_validator=None) -> None:
        self.amr_validator = amr_validator
        super().__init__(
            kind=AuthenticatorKind.FEDERATED_OIDC,
            factor_class=AuthenticationFactorClass.FEDERATED,
            description="Federated OIDC authentication evidence projection.",
        )


__all__ = ["FederatedOidcAuthenticator"]
