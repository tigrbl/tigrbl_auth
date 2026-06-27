"""Local session authenticator provider."""

from __future__ import annotations

from tigrbl_identity_authenticator_bases import AuthenticatorBase
from tigrbl_identity_contracts.authenticators import AuthenticationFactorClass, AuthenticatorKind


class SessionLocalAuthenticator(AuthenticatorBase):
    def __init__(self) -> None:
        super().__init__(
            kind=AuthenticatorKind.SESSION_LOCAL,
            factor_class=AuthenticationFactorClass.POSSESSION,
            description="Local session authentication carrying prior authentication evidence.",
        )


__all__ = ["SessionLocalAuthenticator"]
