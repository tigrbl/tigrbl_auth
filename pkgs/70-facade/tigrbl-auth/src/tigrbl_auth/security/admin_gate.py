"""Compatibility facade for `tigrbl_authz_policy_admin_gate`."""

from tigrbl_auth._split_imports import alias_module as _alias_module

_module = _alias_module(
    __name__,
    "tigrbl_authz_policy_admin_gate",
    "tigrbl-authz-policy-admin-gate",
)
globals().update(_module.__dict__)
