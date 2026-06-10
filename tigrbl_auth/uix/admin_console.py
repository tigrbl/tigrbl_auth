"""Compatibility facade for `tigrbl_identity_operator.uix.admin_console`."""

from tigrbl_auth._split_imports import alias_module as _alias_module

_module = _alias_module(__name__, "tigrbl_identity_operator.uix.admin_console", "tigrbl-identity-operator")
globals().update(_module.__dict__)
