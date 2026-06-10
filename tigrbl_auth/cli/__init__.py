"""Lazy compatibility aliases for the canonical `tigrbl_identity_cli.cli` package."""

from __future__ import annotations

from importlib import import_module as _import_module
import sys as _sys
from types import ModuleType as _ModuleType
from typing import Any

_MODULES = frozenset(
    {
        "artifacts",
        "boundary",
        "certification_evidence",
        "claim_registry",
        "claims",
        "feature_surface",
        "governance",
        "handlers",
        "install_substrate",
        "main",
        "metadata",
        "project_tree",
        "reports",
        "runtime",
        "truth",
    }
)


def _proxy_module(name: str) -> _ModuleType:
    module_name = f"{__name__}.{name}"
    target_name = f"tigrbl_identity_cli.cli.{name}"
    proxy = _ModuleType(module_name)
    proxy.__package__ = __name__
    proxy.__doc__ = f"Lazy compatibility proxy for `{target_name}`."

    def _getattr(attr: str) -> Any:
        target = _import_module(target_name)
        _sys.modules[module_name] = target
        return getattr(target, attr)

    proxy.__getattr__ = _getattr  # type: ignore[attr-defined]
    return proxy


for _name in _MODULES:
    _sys.modules.setdefault(f"{__name__}.{_name}", _proxy_module(_name))


def main(argv: list[str] | None = None) -> int:
    return int(_import_module("tigrbl_identity_cli.cli.main").main(argv))


def __getattr__(name: str) -> Any:
    if name in _MODULES:
        return _sys.modules[f"{__name__}.{name}"]
    raise AttributeError(name)


__all__ = ["main"]
