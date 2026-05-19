"""Legacy import facade for canonical runtime settings.

This compatibility surface intentionally reloads the canonical settings module
when *it* is reloaded so environment-driven helper tests can refresh the active
singleton without importing the entire runtime stack.
"""

from __future__ import annotations

from importlib import import_module, reload as _reload

_settings_module = import_module("tigrbl_auth.config.settings")
_settings_module = _reload(_settings_module)

Settings = _settings_module.Settings
settings = _settings_module.settings

__all__ = ["Settings", "settings"]
