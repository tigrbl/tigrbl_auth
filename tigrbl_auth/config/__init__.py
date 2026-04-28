"""Configuration package exports with minimal import side effects."""

from __future__ import annotations

from importlib import import_module

from .deployment import (
    EXTENSION_REGISTRY,
    PLUGIN_MODE_TO_SURFACE_SETS,
    PROTOCOL_SLICE_REGISTRY,
    ROUTE_REGISTRY,
    SURFACE_SET_REGISTRY,
    resolve_deployment,
)
from .feature_flags import feature_flag_registry, cli_flag_registry, flags_for_profile
from .profile_loader import load_packaged_runtime_profiles, load_runtime_profile
from .surfaces import surface_registry, enabled_surface_summary, surface_set_registry

__all__ = [
    "settings",
    "Settings",
    "feature_flag_registry",
    "cli_flag_registry",
    "flags_for_profile",
    "load_packaged_runtime_profiles",
    "load_runtime_profile",
    "surface_registry",
    "enabled_surface_summary",
    "surface_set_registry",
    "resolve_deployment",
    "SURFACE_SET_REGISTRY",
    "PROTOCOL_SLICE_REGISTRY",
    "EXTENSION_REGISTRY",
    "ROUTE_REGISTRY",
    "PLUGIN_MODE_TO_SURFACE_SETS",
]


def __getattr__(name: str):
    if name in {"settings", "Settings"}:
        module = import_module("tigrbl_auth.config.settings")
        return getattr(module, name)
    raise AttributeError(name)
