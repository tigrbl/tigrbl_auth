"""Compatibility dependency facade for `tigrbl_identity_storage.operator_store`."""

from importlib import import_module as _import_module
import sys as _sys

_module = _import_module("tigrbl_identity_storage.operator_store")
_sys.modules[__name__] = _module
