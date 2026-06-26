"""Compatibility facade for authorization invariant policy surfaces."""

from tigrbl_auth._split_imports import alias_module as _alias_module

_module = _alias_module(
    __name__,
    "tigrbl_authz_policy",
    "tigrbl-authz-policy",
)
globals().update(_module.__dict__)
