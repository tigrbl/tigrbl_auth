"""Compatibility facade for `tba_runtime_identity_storage.session_service`."""

from tba_auth._split_imports import alias_module as _alias_module

_module = _alias_module(__name__, "tba_runtime_identity_storage.session_service", "tba-runtime-identity-storage")
globals().update(_module.__dict__)
