"""Packaged runtime profile loading and validation helpers."""

from __future__ import annotations

from dataclasses import dataclass
from importlib import resources
from pathlib import Path
from typing import Any, Mapping

import yaml

from .deployment import (
    EXTENSION_REGISTRY,
    PLUGIN_MODE_TO_SURFACE_SETS,
    PROTOCOL_SLICE_REGISTRY,
    SURFACE_SET_REGISTRY,
    VALID_PLUGIN_MODES,
    VALID_PROFILES,
    resolve_deployment,
)
from .feature_flags import flags_for_profile


class RuntimeProfileError(ValueError):
    """Raised when a runtime profile file is malformed or inconsistent."""


@dataclass(frozen=True, slots=True)
class RuntimeProfile:
    id: str
    title: str
    ssot_profile_id: str
    feature_id: str
    description: str
    surface_plugin_mode: str
    surface_sets: tuple[str, ...]
    protocol_slices: tuple[str, ...]
    extensions: tuple[str, ...]
    flags_enabled: tuple[str, ...]
    data: Mapping[str, Any]

    def resolve(self):
        return resolve_deployment(
            profile=self.id,
            surface_sets=self.surface_sets,
            protocol_slices=self.protocol_slices,
            extensions=self.extensions,
            plugin_mode=self.surface_plugin_mode,
        )


def _profile_root() -> resources.abc.Traversable:
    return resources.files("tigrbl_auth").joinpath("profiles")


def _read_yaml(path: resources.abc.Traversable | Path) -> Mapping[str, Any]:
    try:
        content = path.read_text(encoding="utf-8")
    except TypeError:
        content = Path(path).read_text(encoding="utf-8")
    loaded = yaml.safe_load(content)
    if not isinstance(loaded, dict):
        raise RuntimeProfileError(f"{path} must contain a YAML mapping")
    return loaded


def _items(value: Any, *, field: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, list):
        raise RuntimeProfileError(f"{field} must be a list")
    items = tuple(str(item) for item in value)
    if any(not item for item in items):
        raise RuntimeProfileError(f"{field} must not contain empty values")
    return items


def validate_profile_data(data: Mapping[str, Any], *, source: str = "<runtime-profile>") -> RuntimeProfile:
    profile_id = str(data.get("id") or "")
    if profile_id not in VALID_PROFILES:
        raise RuntimeProfileError(f"{source} has unknown profile id {profile_id!r}")
    if data.get("schema_version") != "0.1.0":
        raise RuntimeProfileError(f"{source} has unsupported schema_version")

    title = str(data.get("title") or "")
    ssot_profile_id = str(data.get("ssot_profile_id") or "")
    feature_id = str(data.get("feature_id") or "")
    description = str(data.get("description") or "")
    plugin_mode = str(data.get("surface_plugin_mode") or "")
    surface_sets = _items(data.get("surface_sets"), field="surface_sets")
    protocol_slices = _items(data.get("protocol_slices"), field="protocol_slices")
    extensions = _items(data.get("extensions"), field="extensions")
    flags = data.get("flags")
    if not isinstance(flags, dict):
        raise RuntimeProfileError(f"{source} missing flags mapping")
    enabled_flags = _items(flags.get("enabled"), field="flags.enabled")

    required = {
        "title": title,
        "ssot_profile_id": ssot_profile_id,
        "feature_id": feature_id,
        "description": description,
    }
    missing = [name for name, value in required.items() if not value]
    if missing:
        raise RuntimeProfileError(f"{source} missing required fields: {', '.join(missing)}")
    if ssot_profile_id != f"prf:{profile_id}":
        raise RuntimeProfileError(f"{source} ssot_profile_id does not match id")
    if feature_id != f"feat:profile-{profile_id}":
        raise RuntimeProfileError(f"{source} feature_id does not match id")
    if plugin_mode not in VALID_PLUGIN_MODES:
        raise RuntimeProfileError(f"{source} has unknown plugin mode {plugin_mode!r}")

    unknown_surfaces = sorted(set(surface_sets) - set(SURFACE_SET_REGISTRY))
    unknown_slices = sorted(set(protocol_slices) - set(PROTOCOL_SLICE_REGISTRY))
    unknown_extensions = sorted(set(extensions) - set(EXTENSION_REGISTRY))
    if unknown_surfaces:
        raise RuntimeProfileError(f"{source} has unknown surface sets: {', '.join(unknown_surfaces)}")
    if unknown_slices:
        raise RuntimeProfileError(f"{source} has unknown protocol slices: {', '.join(unknown_slices)}")
    if unknown_extensions:
        raise RuntimeProfileError(f"{source} has unknown extensions: {', '.join(unknown_extensions)}")

    allowed_flags = set(flags_for_profile(profile_id))
    disallowed = sorted(flag for flag in enabled_flags if flag not in allowed_flags)
    if disallowed:
        raise RuntimeProfileError(f"{source} enables flags outside profile scope: {', '.join(disallowed)}")

    mode_surfaces = set(PLUGIN_MODE_TO_SURFACE_SETS[plugin_mode])
    if plugin_mode != "mixed" and set(surface_sets) != mode_surfaces:
        raise RuntimeProfileError(f"{source} surface_sets do not match plugin mode {plugin_mode!r}")

    return RuntimeProfile(
        id=profile_id,
        title=title,
        ssot_profile_id=ssot_profile_id,
        feature_id=feature_id,
        description=description,
        surface_plugin_mode=plugin_mode,
        surface_sets=surface_sets,
        protocol_slices=protocol_slices,
        extensions=extensions,
        flags_enabled=enabled_flags,
        data=data,
    )


def load_runtime_profile(profile_id: str) -> RuntimeProfile:
    path = _profile_root().joinpath(f"{profile_id}.yaml")
    if not path.is_file():
        raise RuntimeProfileError(f"runtime profile {profile_id!r} is not packaged")
    return validate_profile_data(_read_yaml(path), source=f"{profile_id}.yaml")


def load_packaged_runtime_profiles() -> dict[str, RuntimeProfile]:
    profiles: dict[str, RuntimeProfile] = {}
    for path in sorted(_profile_root().iterdir(), key=lambda item: item.name):
        if not path.name.endswith((".yaml", ".yml")):
            continue
        profile = validate_profile_data(_read_yaml(path), source=path.name)
        if profile.id in profiles:
            raise RuntimeProfileError(f"duplicate runtime profile id {profile.id!r}")
        profiles[profile.id] = profile
    missing = sorted(set(VALID_PROFILES) - set(profiles))
    if missing:
        raise RuntimeProfileError(f"missing packaged runtime profiles: {', '.join(missing)}")
    return profiles


__all__ = [
    "RuntimeProfile",
    "RuntimeProfileError",
    "load_packaged_runtime_profiles",
    "load_runtime_profile",
    "validate_profile_data",
]
