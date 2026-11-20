"""Compatibility facade for `tba_protocol_oauth.standards.dpop`."""

from tba_auth._split_imports import alias_module as _alias_module

_module = _alias_module(__name__, "tba_protocol_oauth.standards.dpop", "tba-protocol-oauth")
globals().update(_module.__dict__)
