"""Compatibility facade for runtime-owned lifecycle adapters."""

from tigrbl_auth._split_imports import alias_module as _alias_module

_module = _alias_module(
    __name__,
    "tigrbl_identity_storage_runtime.persistence",
    "tigrbl-identity-storage-runtime",
)
globals().update(_module.__dict__)
