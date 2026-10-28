"""Compatibility facade for `tba_router_admin_gate`."""

from tba_auth._split_imports import alias_module as _alias_module

_module = _alias_module(
    __name__,
    "tba_router_admin_gate",
    "tigrbl-authz-policy-admin-gate",
)
globals().update(_module.__dict__)
