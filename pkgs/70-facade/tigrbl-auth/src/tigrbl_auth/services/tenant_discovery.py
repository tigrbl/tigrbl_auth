"""Compatibility facade for `tigrbl_identity_principals.tenant_discovery`."""

from tigrbl_auth._split_imports import alias_module as _alias_module

_module = _alias_module(
    __name__,
    "tigrbl_identity_principals.tenant_discovery",
    "tigrbl-identity-principals",
)
globals().update(_module.__dict__)
