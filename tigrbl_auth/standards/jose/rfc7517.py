"""Compatibility facade for `tigrbl_identity_jose.standards.rfc7517`."""

from tigrbl_auth._split_imports import alias_module as _alias_module

_module = _alias_module(
    __name__,
    "tigrbl_identity_jose.standards.rfc7517",
    "tigrbl-identity-jose",
)
globals().update(_module.__dict__)
