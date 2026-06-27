"""Federated OIDC authenticator provider."""

from __future__ import annotations

from tigrbl_identity_authenticator_bases import AmrEmitterMixin, AuthenticatorBase
from tigrbl_identity_contracts.authenticators import AuthenticationFactorClass, AuthenticatorKind


class FederatedOidcAuthenticator(AmrEmitterMixin, AuthenticatorBase):
    def __init__(self, *, amr_validator=None) -> None:
        self.amr_validator = amr_validator
        super().__init__(
            kind=AuthenticatorKind.FEDERATED_OIDC,
            factor_class=AuthenticationFactorClass.FEDERATED,
            description="Federated OIDC authentication evidence projection.",
        )


__all__ = ["FederatedOidcAuthenticator"]
