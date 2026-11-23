"""Helpers for legacy facade modules that alias split packages."""

from __future__ import annotations

from importlib import import_module
from pathlib import Path
import sys
from types import ModuleType


def _repo_root() -> Path | None:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pkgs").is_dir():
            return parent
    return None


def ensure_split_package_importable(import_root: str, dist_name: str) -> None:
    try:
        import_module(import_root)
        return
    except ModuleNotFoundError as exc:
        if exc.name != import_root:
            raise

    root = _repo_root()
    if root is not None:
        src = root / "pkgs" / dist_name / "src"
        if src.exists():
            value = str(src)
            if value not in sys.path:
                sys.path.insert(0, value)

    import_module(import_root)


def alias_module(legacy_name: str, canonical_module: str, dist_name: str) -> ModuleType:
    ensure_split_package_importable(canonical_module.split(".", 1)[0], dist_name)
    module = import_module(canonical_module)
    sys.modules[legacy_name] = module
    return module


__all__ = ["alias_module", "ensure_split_package_importable"]
