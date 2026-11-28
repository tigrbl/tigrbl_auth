"""Compatibility facade for authorization invariant policy surfaces."""

from tba_auth._split_imports import alias_module as _alias_module

_module = _alias_module(
    __name__,
    "tba_runtime_authorization_policy",
    "tba-runtime-authorization-policy",
)
globals().update(_module.__dict__)
