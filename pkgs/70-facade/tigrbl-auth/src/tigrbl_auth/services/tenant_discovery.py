"""Compatibility facade for `tigrbl_auth_protocol_oidc.tenant_discovery`."""

from tigrbl_auth._split_imports import alias_module as _alias_module

_module = _alias_module(
    __name__,
    "tigrbl_auth_protocol_oidc.tenant_discovery",
    "tigrbl-auth-protocol-oidc",
)
globals().update(_module.__dict__)
