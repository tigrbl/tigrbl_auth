"""Compatibility facade for `tba_operator_identity.uix.admin_console`."""

from tba_auth._split_imports import alias_module as _alias_module

_module = _alias_module(
    __name__,
    "tba_operator_identity.uix.admin_console",
    "tba-operator-identity",
)
globals().update(_module.__dict__)
