"""Compatibility facade for `tigrbl_authz_policy.certification`."""

from tigrbl_auth._split_imports import alias_module as _alias_module

_module = _alias_module(__name__, "tigrbl_authz_policy.certification", "tigrbl-authz-policy")
globals().update(_module.__dict__)
