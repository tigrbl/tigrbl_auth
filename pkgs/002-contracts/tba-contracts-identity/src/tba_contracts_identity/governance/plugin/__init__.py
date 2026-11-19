"""Plugin and SDK governance contract dataclasses."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True, slots=True)
class SDKPackage:
    sdk_id: str
    package_name: str
    language: str
    version: str
    compatible_runtime_range: tuple[str, str]
    generated_contracts: Mapping[str, str]
    auth_helpers: tuple[str, ...]
    supported_errors: tuple[str, ...]
    release_channel: str = "stable"


@dataclass(frozen=True, slots=True)
class PluginDescriptor:
    plugin_id: str
    name: str
    version: str
    extension_points: tuple[str, ...]
    lifecycle_hooks: tuple[str, ...]
    compatible_sdk_ids: tuple[str, ...]
    isolation_mode: str
    operator_controls: tuple[str, ...]
    fail_behavior: str
    registered_at: str
    enabled: bool = True


@dataclass(frozen=True, slots=True)
class PluginLifecycleEvent:
    event_id: str
    plugin_id: str
    hook_name: str
    outcome: str
    message: str
    recorded_at: str


__all__ = [
    "PluginDescriptor",
    "PluginLifecycleEvent",
    "SDKPackage",
]
