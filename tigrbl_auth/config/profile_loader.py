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
    base_profile: str
    ssot_profile_id: str
    feature_id: str
    description: str
    surface_plugin_mode: str
    surface_sets: tuple[str, ...]
    protocol_slices: tuple[str, ...]
    extensions: tuple[str, ...]
    flags_enabled: tuple[str, ...]
    data: Mapping[str, Any]
    source_kind: str = "packaged-profile-id"
    source_path: str | None = None

    def resolve(self):
        return resolve_deployment(
            profile=self.base_profile,
            surface_sets=self.surface_sets,
            protocol_slices=self.protocol_slices,
            extensions=self.extensions,
            plugin_mode=self.surface_plugin_mode,
            flag_overrides=self.flag_overrides(),
            profile_source=self.provenance(),
        )

    def flag_overrides(self) -> dict[str, Any]:
        overrides: dict[str, Any] = {name: True for name in self.flags_enabled}
        security = self.data.get("security")
        if isinstance(security, Mapping) and "strict_boundary_enforcement" in security:
            overrides["strict_boundary_enforcement"] = bool(security["strict_boundary_enforcement"])
        return overrides

    def provenance(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "kind": self.source_kind,
            "profile_id": self.id,
            "base_profile": self.base_profile,
            "applied_override_keys": sorted(self.flags_enabled),
            "redaction": "no-secret-values-emitted",
        }
        if self.source_path:
            payload["path"] = self.source_path
        return payload


def _profile_root() -> resources.abc.Traversable:
    return resources.files("tigrbl_auth").joinpath("profiles")


def _read_yaml(path: resources.abc.Traversable | Path) -> Mapping[str, Any]:
    try:
        content = path.read_text(encoding="utf-8")
    except TypeError:
        content = Path(path).read_text(encoding="utf-8")
    try:
        loaded = yaml.safe_load(content)
    except yaml.YAMLError as exc:
        raise RuntimeProfileError(f"{path} must contain a YAML mapping") from exc
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


def validate_profile_data(
    data: Mapping[str, Any],
    *,
    source: str = "<runtime-profile>",
    external: bool = False,
) -> RuntimeProfile:
    allowed_external_keys = {
        "schema_version",
        "id",
        "title",
        "base_profile",
        "description",
        "surface_plugin_mode",
        "surfaces",
        "surface_sets",
        "flags",
        "protocol_slices",
        "extensions",
        "security",
        "contracts",
        "x-tigrbl-auth",
    }
    if external:
        unknown = sorted(set(data) - allowed_external_keys)
        if unknown:
            raise RuntimeProfileError(f"{source} has unknown top-level fields: {', '.join(unknown)}")

    profile_id = str(data.get("id") or "")
    base_profile = str(data.get("base_profile") or profile_id)
    if (not external and profile_id not in VALID_PROFILES) or base_profile not in VALID_PROFILES:
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

    if external:
        for field_name in ("base_profile", "surfaces", "security", "contracts"):
            if field_name not in data:
                raise RuntimeProfileError(f"{source} missing required field: {field_name}")
        if not isinstance(data.get("surfaces"), Mapping):
            raise RuntimeProfileError(f"{source} surfaces must be a mapping")
        if not isinstance(data.get("security"), Mapping):
            raise RuntimeProfileError(f"{source} security must be a mapping")
        if not isinstance(data.get("contracts"), Mapping):
            raise RuntimeProfileError(f"{source} contracts must be a mapping")

    required = {
        "title": title,
        "description": description,
    }
    if not external:
        required["ssot_profile_id"] = ssot_profile_id
        required["feature_id"] = feature_id
    missing = [name for name, value in required.items() if not value]
    if missing:
        raise RuntimeProfileError(f"{source} missing required fields: {', '.join(missing)}")
    if not external and ssot_profile_id != f"prf:{profile_id}":
        raise RuntimeProfileError(f"{source} ssot_profile_id does not match id")
    if not external and feature_id != f"feat:profile-{profile_id}":
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

    allowed_flags = set(flags_for_profile(base_profile))
    disallowed = sorted(flag for flag in enabled_flags if flag not in allowed_flags)
    if disallowed:
        raise RuntimeProfileError(f"{source} enables flags outside profile scope: {', '.join(disallowed)}")

    mode_surfaces = set(PLUGIN_MODE_TO_SURFACE_SETS[plugin_mode])
    if plugin_mode != "mixed" and set(surface_sets) != mode_surfaces:
        raise RuntimeProfileError(f"{source} surface_sets do not match plugin mode {plugin_mode!r}")

    return RuntimeProfile(
        id=profile_id,
        title=title,
        base_profile=base_profile,
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


def _looks_like_path(reference: str) -> bool:
    value = reference.strip()
    return (
        value.endswith((".yaml", ".yml"))
        or "/" in value
        or "\\" in value
        or value.startswith(".")
    )


def load_external_runtime_profile(path: str | Path) -> RuntimeProfile:
    external_path = Path(path).expanduser()
    if not external_path.exists():
        raise RuntimeProfileError(f"external runtime profile path does not exist: {external_path}")
    if not external_path.is_file():
        raise RuntimeProfileError(f"external runtime profile path is not a file: {external_path}")
    if external_path.suffix.lower() not in {".yaml", ".yml"}:
        raise RuntimeProfileError(f"external runtime profile path must end in .yaml or .yml: {external_path}")
    profile = validate_profile_data(_read_yaml(external_path), source=str(external_path), external=True)
    return RuntimeProfile(
        id=profile.id,
        title=profile.title,
        base_profile=profile.base_profile,
        ssot_profile_id=profile.ssot_profile_id,
        feature_id=profile.feature_id,
        description=profile.description,
        surface_plugin_mode=profile.surface_plugin_mode,
        surface_sets=profile.surface_sets,
        protocol_slices=profile.protocol_slices,
        extensions=profile.extensions,
        flags_enabled=profile.flags_enabled,
        data=profile.data,
        source_kind="external-profile-path",
        source_path=str(external_path.resolve()),
    )


def load_profile_reference(reference: str | None) -> RuntimeProfile:
    value = str(reference or "baseline").strip() or "baseline"
    if value in VALID_PROFILES:
        profile = load_runtime_profile(value)
        return RuntimeProfile(
            id=profile.id,
            title=profile.title,
            base_profile=profile.base_profile,
            ssot_profile_id=profile.ssot_profile_id,
            feature_id=profile.feature_id,
            description=profile.description,
            surface_plugin_mode=profile.surface_plugin_mode,
            surface_sets=profile.surface_sets,
            protocol_slices=profile.protocol_slices,
            extensions=profile.extensions,
            flags_enabled=profile.flags_enabled,
            data=profile.data,
            source_kind="packaged-profile-id",
        )
    if _looks_like_path(value):
        return load_external_runtime_profile(value)
    raise RuntimeProfileError(f"unknown packaged runtime profile id {value!r}")


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
    "load_external_runtime_profile",
    "load_packaged_runtime_profiles",
    "load_profile_reference",
    "load_runtime_profile",
    "validate_profile_data",
]
