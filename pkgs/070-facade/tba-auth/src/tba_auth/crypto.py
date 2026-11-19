"""Compatibility alias for the environment-backed JOSE crypto provider."""

from importlib import import_module
import sys

_implementation = import_module("tba_provider_identity_jose.crypto")
sys.modules[__name__] = _implementation
