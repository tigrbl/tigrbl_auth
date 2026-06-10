"""Compatibility facade for `tigrbl_identity_policy.admin_gate`."""

from tigrbl_auth._split_imports import alias_module as _alias_module

_module = _alias_module(__name__, "tigrbl_identity_policy.admin_gate", "tigrbl-identity-policy")
globals().update(_module.__dict__)
