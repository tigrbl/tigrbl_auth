"""Compatibility facade for `tigrbl_authz_policy_concrete.invariant_registry`."""

from tigrbl_auth._split_imports import alias_module as _alias_module

_module = _alias_module(
    __name__,
    "tigrbl_authz_policy_concrete.invariant_registry",
    "tigrbl-authz-policy-concrete",
)
globals().update(_module.__dict__)
