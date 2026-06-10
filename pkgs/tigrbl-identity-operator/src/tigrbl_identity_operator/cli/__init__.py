"""Compatibility aliases for the canonical `tigrbl_identity_cli.cli` package."""

from __future__ import annotations

from importlib import import_module as _import_module
import sys as _sys

_MODULES = ('artifacts', 'boundary', 'certification_evidence', 'claim_registry', 'claims', 'feature_surface', 'governance', 'handlers', 'install_substrate', 'main', 'metadata', 'project_tree', 'reports', 'runtime', 'truth')

for _name in _MODULES:
    _module = _import_module(f"tigrbl_identity_cli.cli.{_name}")
    _sys.modules[f"{__name__}.{_name}"] = _module
    globals()[_name] = _module

main = globals()["main"].main

__all__ = ["main"]
