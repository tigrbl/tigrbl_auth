"""Compatibility facade for `tigrbl_identity_oauth.ops.register`."""

from tigrbl_auth._split_imports import alias_module as _alias_module

_module = _alias_module(__name__, "tigrbl_identity_oauth.ops.register", "tigrbl-identity-oauth")
globals().update(_module.__dict__)
