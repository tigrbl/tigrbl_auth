"""Remote introspection authenticator provider."""

from __future__ import annotations

from tigrbl_identity_authenticator_bases import AuthenticatorBase, RemoteIntrospectionMixin
from tigrbl_identity_contracts.authenticators import AuthenticationFactorClass, AuthenticatorKind


class RemoteIntrospectionAuthenticator(RemoteIntrospectionMixin, AuthenticatorBase):
    def __init__(self) -> None:
        super().__init__(
            kind=AuthenticatorKind.REMOTE_INTROSPECTION,
            factor_class=AuthenticationFactorClass.FEDERATED,
            description="Remote authentication or token introspection.",
        )


__all__ = ["RemoteIntrospectionAuthenticator"]
