"""Compatibility facade for `tba_runtime_authorization_policy.provenance`."""

from tba_auth._split_imports import alias_module as _alias_module

_module = _alias_module(__name__, "tba_runtime_authorization_policy.provenance", "tba-runtime-authorization-policy")
globals().update(_module.__dict__)
