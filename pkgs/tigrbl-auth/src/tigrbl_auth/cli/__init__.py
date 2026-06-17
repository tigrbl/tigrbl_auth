"""Lazy compatibility aliases for the canonical `tigrbl_identity_cli.cli` package."""

from __future__ import annotations

from importlib import import_module as _import_module
from pathlib import Path as _Path
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


def _repo_root() -> _Path | None:
    for parent in _Path(__file__).resolve().parents:
        if (parent / "pkgs").is_dir():
            return parent
    return None


def _prefer_workspace_split_cli() -> None:
    root = _repo_root()
    if root is None:
        return

    src = root / "pkgs" / "tigrbl-identity-cli" / "src"
    if not src.exists():
        return

    src_value = str(src)
    if src_value in _sys.path:
        _sys.path.remove(src_value)
    _sys.path.insert(0, src_value)

    for module_name, module in list(_sys.modules.items()):
        if module_name != "tigrbl_identity_cli" and not module_name.startswith("tigrbl_identity_cli."):
            continue
        module_file = getattr(module, "__file__", None)
        if module_file is None:
            continue
        try:
            if not _Path(module_file).resolve().is_relative_to(src.resolve()):
                _sys.modules.pop(module_name, None)
        except OSError:
            _sys.modules.pop(module_name, None)


def _import_target(name: str) -> _ModuleType:
    _prefer_workspace_split_cli()
    return _import_module(f"tigrbl_identity_cli.cli.{name}")


def _proxy_module(name: str) -> _ModuleType:
    module_name = f"{__name__}.{name}"
    target_name = f"tigrbl_identity_cli.cli.{name}"
    proxy = _ModuleType(module_name)
    proxy.__package__ = __name__
    proxy.__doc__ = f"Lazy compatibility proxy for `{target_name}`."

    def _getattr(attr: str) -> Any:
        target = _import_target(name)
        _sys.modules[module_name] = target
        return getattr(target, attr)

    proxy.__getattr__ = _getattr  # type: ignore[attr-defined]
    return proxy


for _name in _MODULES:
    _sys.modules.setdefault(f"{__name__}.{_name}", _proxy_module(_name))


def main(argv: list[str] | None = None) -> int:
    return int(_import_target("main").main(argv))


def __getattr__(name: str) -> Any:
    if name in _MODULES:
        return _sys.modules[f"{__name__}.{name}"]
    raise AttributeError(name)


__all__ = ["main"]
