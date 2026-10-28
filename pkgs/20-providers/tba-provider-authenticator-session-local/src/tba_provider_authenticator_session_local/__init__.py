"""Local session authenticator provider."""

from __future__ import annotations

from tba_bases_authenticator import AuthenticatorBase
from tba_contracts_identity.authenticators import AuthenticationFactorClass, AuthenticatorKind


class SessionLocalAuthenticator(AuthenticatorBase):
    def __init__(self) -> None:
        super().__init__(
            kind=AuthenticatorKind.SESSION_LOCAL,
            factor_class=AuthenticationFactorClass.POSSESSION,
            description="Local session authentication carrying prior authentication evidence.",
        )


__all__ = ["SessionLocalAuthenticator"]
