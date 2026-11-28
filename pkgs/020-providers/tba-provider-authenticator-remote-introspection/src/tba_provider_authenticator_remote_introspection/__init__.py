"""Remote introspection authenticator provider."""

from __future__ import annotations

from tba_bases_authenticator import AuthenticatorBase, RemoteIntrospectionMixin
from tba_contracts_identity.authenticators import AuthenticationFactorClass, AuthenticatorKind


class RemoteIntrospectionAuthenticator(RemoteIntrospectionMixin, AuthenticatorBase):
    def __init__(self) -> None:
        super().__init__(
            kind=AuthenticatorKind.REMOTE_INTROSPECTION,
            factor_class=AuthenticationFactorClass.FEDERATED,
            description="Remote authentication or token introspection.",
        )


__all__ = ["RemoteIntrospectionAuthenticator"]
