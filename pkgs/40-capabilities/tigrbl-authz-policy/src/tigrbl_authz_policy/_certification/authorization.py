"""Compatibility alias for `tigrbl_auth_release_certification.certification.authorization`."""

from __future__ import annotations

from importlib import import_module as _import_module
import sys as _sys

_target = _import_module("tigrbl_auth_release_certification.certification.authorization")
_sys.modules[__name__] = _target
globals().update(_target.__dict__)
