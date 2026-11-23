"""Compatibility alias for TBA's internal JOSE key manager."""
from importlib import import_module
import sys

_implementation = import_module("tba_provider_identity_jose.key_management")
sys.modules[__name__] = _implementation
