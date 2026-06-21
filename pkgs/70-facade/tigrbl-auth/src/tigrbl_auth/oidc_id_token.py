"""Compatibility facade for `tigrbl_auth_protocol_oidc.id_token`."""

from tigrbl_auth._split_imports import alias_module as _alias_module

_module = _alias_module(
    __name__,
    "tigrbl_auth_protocol_oidc.id_token",
    "tigrbl-auth-protocol-oidc",
)
globals().update(_module.__dict__)
