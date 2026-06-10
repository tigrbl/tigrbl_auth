"""Compatibility dependency facade for `tigrbl_identity_jose.key_management`."""

from importlib import import_module as _import_module
import sys as _sys

_module = _import_module("tigrbl_identity_jose.key_management")
_sys.modules[__name__] = _module
