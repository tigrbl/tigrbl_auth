"""Compatibility facade for `tba_protocol_oauth.standards.resource_verifier_contract`."""

from tba_auth._split_imports import alias_module as _alias_module

_module = _alias_module(
    __name__,
    "tba_protocol_oauth.standards.resource_verifier_contract",
    "tba-protocol-oauth",
)
globals().update(_module.__dict__)
