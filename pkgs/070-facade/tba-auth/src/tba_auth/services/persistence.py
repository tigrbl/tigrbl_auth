"""Compatibility facade for runtime-owned lifecycle adapters."""

from tba_auth._split_imports import alias_module as _alias_module

_module = _alias_module(
    __name__,
    "tba_runtime_identity_storage.persistence",
    "tba-runtime-identity-storage",
)
globals().update(_module.__dict__)
