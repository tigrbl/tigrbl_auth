"""Compatibility facade for `tigrbl_authz_policy.provenance`."""

from tigrbl_auth._split_imports import alias_module as _alias_module

_module = _alias_module(__name__, "tigrbl_authz_policy.provenance", "tigrbl-authz-policy")
globals().update(_module.__dict__)
