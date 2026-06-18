"""Compatibility facade for protocol REST schemas."""

from tigrbl_auth._split_imports import alias_module as _alias_module

_module = _alias_module(
    __name__,
    "tigrbl_identity_contracts.rest",
    "tigrbl-identity-contracts",
)
globals().update(_module.__dict__)
