"""Compatibility alias for Tigrbl Auth's internal JOSE key manager."""
from importlib import import_module
import sys

_implementation = import_module("tigrbl_identity_jose.key_management")
sys.modules[__name__] = _implementation
