"""Compatibility facade for `tigrbl_identity_storage.operator_store`."""

from tigrbl_auth._split_imports import alias_module as _alias_module

_module = _alias_module(__name__, "tigrbl_identity_storage.operator_store", "tigrbl-identity-storage")
globals().update(_module.__dict__)
