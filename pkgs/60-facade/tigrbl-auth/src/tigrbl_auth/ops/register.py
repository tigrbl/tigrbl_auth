"""Compatibility facade for `tigrbl_auth_protocol_oauth.ops.register`."""

from tigrbl_auth._split_imports import alias_module as _alias_module

_module = _alias_module(__name__, "tigrbl_auth_protocol_oauth.ops.register", "tigrbl-auth-protocol-oauth")
globals().update(_module.__dict__)
