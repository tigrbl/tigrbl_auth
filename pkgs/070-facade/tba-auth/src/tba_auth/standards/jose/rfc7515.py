"""Compatibility facade for `tba_provider_identity_jose.standards.rfc7515`."""

from tba_auth._split_imports import alias_module as _alias_module

_module = _alias_module(
    __name__,
    "tba_provider_identity_jose.standards.rfc7515",
    "tba-provider-identity-jose",
)
globals().update(_module.__dict__)
