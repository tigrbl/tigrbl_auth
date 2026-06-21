"""Compatibility facade for `tigrbl_auth_protocol_oauth.standards.oauth_security_bcp`."""

from tigrbl_auth._split_imports import alias_module as _alias_module

_module = _alias_module(__name__, "tigrbl_auth_protocol_oauth.standards.oauth_security_bcp", "tigrbl-auth-protocol-oauth")
globals().update(_module.__dict__)
