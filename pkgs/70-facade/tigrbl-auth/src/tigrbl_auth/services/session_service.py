"""Compatibility facade for `tigrbl_identity_storage_runtime.session_service`."""

from tigrbl_auth._split_imports import alias_module as _alias_module

_module = _alias_module(__name__, "tigrbl_identity_storage_runtime.session_service", "tigrbl-identity-storage-runtime")
globals().update(_module.__dict__)
