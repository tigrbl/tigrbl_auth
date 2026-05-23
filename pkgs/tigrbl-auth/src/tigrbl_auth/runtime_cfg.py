"""Compatibility facade for runtime settings."""

from __future__ import annotations

import sys
from importlib import import_module, reload as _reload
from pathlib import Path


def _ensure_runtime_source_path() -> None:
    package_src = Path(__file__).resolve().parents[2]
    pkgs_root = package_src.parent.parent
    runtime_src = pkgs_root / "tigrbl-identity-runtime" / "src"
    value = str(runtime_src)
    if runtime_src.exists() and value not in sys.path:
        sys.path.insert(0, value)


_ensure_runtime_source_path()
_settings_module = import_module("tigrbl_identity_runtime.settings")
_settings_module = _reload(_settings_module)

Settings = _settings_module.Settings
settings = _settings_module.settings

__all__ = ["Settings", "settings"]
