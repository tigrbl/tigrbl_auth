"""Compatibility facade for `tba_primitives_identity.errors`."""

from tba_auth._split_imports import alias_module as _alias_module

_module = _alias_module(__name__, "tba_primitives_identity.errors", "tba-primitives-identity")
globals().update(_module.__dict__)
