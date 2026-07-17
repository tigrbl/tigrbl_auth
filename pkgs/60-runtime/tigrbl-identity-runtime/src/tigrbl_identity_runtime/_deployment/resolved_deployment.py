from __future__ import annotations
# ruff: noqa: F403,F405

from dataclasses import dataclass, field
from typing import Any

from tigrbl_identity_runtime.feature_flags import flags_for_profile

from .defaults import *
from .product_surfaces import *


@dataclass(slots=True, frozen=True)
class ResolvedDeployment:
    profile: str
    plugin_mode: str
    runtime_style: str
    surface_sets: tuple[str, ...]
    protocol_slices: tuple[str, ...]
    extensions: tuple[str, ...]
    issuer: str
    protected_resource_identifier: str
    strict_boundary_enforcement: bool
    surfaces: dict[str, bool | str]
    flags: dict[str, bool | str]
    active_capabilities: tuple[str, ...]
    active_routes: tuple[str, ...]
    active_contract_routes: tuple[str, ...]
    active_discovery_routes: tuple[str, ...]
    active_targets: tuple[str, ...]
    product_surface: str | None = None
    router_packages: tuple[str, ...] = ()
    allowed_admin_resources: tuple[str, ...] = ()
    required_table_resources: tuple[str, ...] = ()
    allowed_admin_rest_groups: tuple[str, ...] = ()
    profile_source: dict[str, Any] = field(default_factory=dict)

    def flag_enabled(self, name: str) -> bool:
        return bool(self.flags.get(name, False))

    def surface_enabled(self, name: str) -> bool:
        if name in SURFACE_SET_REGISTRY:
            return name in self.surface_sets
        mapping = {
            "public-rest": "surface_public_enabled",
            "admin-rest": "surface_admin_enabled",
            "diagnostics": "surface_diagnostics_enabled",
            "operator": "surface_operator_enabled",
        }
        return bool(self.surfaces.get(mapping.get(name, name), False))

    def route_enabled(self, path: str) -> bool:
        return path in self.active_routes

    def capability_enabled(self, name: str) -> bool:
        return name in self.active_capabilities

    def contract_route_enabled(self, path: str) -> bool:
        return path in self.active_contract_routes

    def discovery_route_enabled(self, path: str) -> bool:
        return path in self.active_discovery_routes

    def target_enabled(self, label: str) -> bool:
        return label in self.active_targets

    def admin_resource_enabled(self, name: str) -> bool:
        if self.product_surface is None:
            return True
        return name in self.allowed_admin_resources

    def admin_rest_group_enabled(self, name: str) -> bool:
        if self.product_surface is None:
            return True
        return name in self.allowed_admin_rest_groups

    def to_manifest(self) -> dict[str, Any]:
        return {
            "profile": self.profile,
            "plugin_mode": self.plugin_mode,
            "runtime_style": self.runtime_style,
            "surface_sets": list(self.surface_sets),
            "protocol_slices": list(self.protocol_slices),
            "extensions": list(self.extensions),
            "issuer": self.issuer,
            "protected_resource_identifier": self.protected_resource_identifier,
            "strict_boundary_enforcement": self.strict_boundary_enforcement,
            "surfaces": self.surfaces,
            "flags": self.flags,
            "active_capabilities": list(self.active_capabilities),
            "active_routes": list(self.active_routes),
            "active_contract_routes": list(self.active_contract_routes),
            "active_discovery_routes": list(self.active_discovery_routes),
            "active_targets": list(self.active_targets),
            "product_surface": self.product_surface,
            "router_packages": list(self.router_packages),
            "allowed_admin_resources": list(self.allowed_admin_resources),
            "required_table_resources": list(self.required_table_resources),
            "allowed_admin_rest_groups": list(self.allowed_admin_rest_groups),
            "profile_source": self.profile_source,
        }


def _csv_items(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        parts = [item.strip() for item in value.split(",")]
        return tuple(item for item in parts if item)
    if isinstance(value, (list, tuple, set)):
        return tuple(str(item).strip() for item in value if str(item).strip())
    return ()


def _settings_dict(settings_obj: object | None) -> dict[str, Any]:
    data = dict(DEFAULT_VALUES)
    if settings_obj is None:
        return data
    for key in DEFAULT_VALUES:
        if hasattr(settings_obj, key):
            data[key] = getattr(settings_obj, key)
    return data


def _all_profile_flags() -> set[str]:
    names: set[str] = set()
    for profile in ("baseline", "production", "hardening", "fapi2-security"):
        names.update(flags_for_profile(profile))
    return names


def _valid_or_default(value: str, allowed: tuple[str, ...], default: str) -> str:
    return value if value in allowed else default


def _expand_product_surface_sets(names: tuple[str, ...]) -> tuple[str, ...]:
    expanded: list[str] = []
    for name in names:
        product_meta = PRODUCT_SURFACE_REGISTRY.get(name)
        if product_meta is not None:
            expanded.extend(str(item) for item in product_meta.get("surface_sets", ()))
        elif name in SURFACE_SET_REGISTRY:
            expanded.append(name)
    return tuple(dict.fromkeys(expanded))


def _product_config(name: str | None) -> dict[str, Any] | None:
    if name is None:
        return None
    try:
        return PRODUCT_SURFACE_REGISTRY[name]
    except KeyError as exc:
        raise ValueError(f"unknown tigrbl_auth product surface: {name}") from exc


def _capability_allowed(capability: str, product_meta: dict[str, Any] | None) -> bool:
    if product_meta is None:
        return True
    allowed = product_meta.get("allowed_capabilities")
    if allowed is None:
        return True
    return capability in set(str(item) for item in allowed)


def _plugin_mode_for_surface_sets(surface_sets: tuple[str, ...]) -> str:
    surface_set = set(surface_sets)
    if surface_set == {"public-rest"}:
        return "public-only"
    if surface_set == {"admin-rest"}:
        return "admin-only"
    if surface_set == {"diagnostics"}:
        return "diagnostics-only"
    return "mixed"


def _derive_surface_sets(
    raw: dict[str, Any], plugin_mode: str, requested: tuple[str, ...]
) -> tuple[str, ...]:
    if requested:
        return _expand_product_surface_sets(
            tuple(name for name in requested if name in SURFACE_SET_REGISTRY)
        )
    if plugin_mode != "mixed":
        return PLUGIN_MODE_TO_SURFACE_SETS[plugin_mode]
    if str(raw.get("surface_plugin_mode", "")) == "mixed":
        return PLUGIN_MODE_TO_SURFACE_SETS["mixed"]
    derived: list[str] = []
    if raw.get("surface_public_enabled", True):
        derived.append("public-rest")
    if raw.get("surface_admin_enabled", True):
        derived.append("admin-rest")
    if raw.get("surface_diagnostics_enabled", True):
        derived.append("diagnostics")
    return tuple(dict.fromkeys(derived))


def _derive_protocol_slices(
    raw: dict[str, Any], allowed_profile_flags: set[str], requested: tuple[str, ...]
) -> tuple[str, ...]:
    if requested:
        return tuple(name for name in requested if name in PROTOCOL_SLICE_REGISTRY)
    derived: list[str] = []
    for name, meta in PROTOCOL_SLICE_REGISTRY.items():
        flags = tuple(meta.get("flags", ()))
        if flags and all(
            flag in allowed_profile_flags and bool(raw.get(flag, False))
            for flag in flags
        ):
            derived.append(name)
    return tuple(derived)


def _derive_extensions(
    raw: dict[str, Any], requested: tuple[str, ...]
) -> tuple[str, ...]:
    if requested:
        return tuple(name for name in requested if name in EXTENSION_REGISTRY)
    derived: list[str] = []
    for name, meta in EXTENSION_REGISTRY.items():
        flags = tuple(meta.get("flags", ()))
        if not flags:
            continue
        if all(bool(raw.get(flag, False)) for flag in flags):
            derived.append(name)
    return tuple(derived)
