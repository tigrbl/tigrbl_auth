"""Pure deployment-resolution helpers for profiles, surfaces, slices, and boundaries.

This module intentionally avoids importing runtime-heavy dependencies so that
contracts, claims, evidence manifests, and governance tooling can resolve the
active deployment shape without initializing the full Tigrbl/SQLAlchemy stack.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Final

from .feature_flags import FEATURE_FLAG_GROUPS, flags_for_profile
from .surfaces import (
    all_surface_capability_registry,
    route_registry as surface_route_registry,
)
from tigrbl_auth.api.rpc import get_rpc_method_registry

# ---------------------------------------------------------------------------
# Pure defaults mirrored from ``config.settings`` for governance tooling.
# ---------------------------------------------------------------------------
DEFAULT_VALUES: Final[dict[str, Any]] = {
    "deployment_profile": "baseline",
    "issuer": "https://authn.example.com",
    "protected_resource_identifier": "https://authn.example.com/resource",
    "strict_boundary_enforcement": True,
    "surface_public_enabled": True,
    "surface_admin_enabled": False,
    "surface_operator_enabled": True,
    "surface_rpc_enabled": False,
    "surface_diagnostics_enabled": False,
    "surface_plugin_mode": "public-only",
    "runtime_style": "standalone",
    "active_surface_sets": "",
    "active_protocol_slices": "",
    "active_extensions": "",
    "jwt_secret": "insecure-dev-secret",
    "log_level": "INFO",
    "enable_id_token_encryption": False,
    "require_tls": True,
    "session_cookie_name": "sid",
    "session_cookie_path": "/",
    "session_cookie_domain": None,
    "session_cookie_samesite": "lax",
    "session_cookie_max_age_seconds": 3600,
    "session_cookie_renewal_seconds": 900,
    "session_cookie_cross_site": False,
    "session_cookie_force_secure": True,
    "enable_rfc6749": True,
    "enable_rfc6750": True,
    "enable_rfc6750_query": False,
    "enable_rfc6750_form": False,
    "enable_rfc7636": True,
    "enable_rfc8414": True,
    "enable_rfc8615": True,
    "enable_rfc7515": True,
    "enable_rfc7516": True,
    "enable_rfc7517": True,
    "enable_rfc7518": True,
    "enable_rfc7519": True,
    "enable_rfc7520": True,
    "enable_rfc7638": True,
    "enable_rfc8037": True,
    "enable_rfc8176": True,
    "enable_rfc8725": True,
    "enable_rfc7009": True,
    "enable_rfc7521": True,
    "enable_rfc7523": True,
    "enable_rfc7591": True,
    "enable_rfc7592": True,
    "enable_rfc7662": True,
    "enforce_rfc8252": True,
    "enable_rfc8252": True,
    "enable_rfc9068": False,
    "enable_rfc9207": True,
    "enable_rfc9728": True,
    "enable_oidc_core": True,
    "enable_oidc_discovery": True,
    "enable_oidc_userinfo": True,
    "enable_oidc_session_management": True,
    "enable_oidc_rp_initiated_logout": True,
    "enable_rfc8628": True,
    "enable_rfc8693": True,
    "enable_rfc8705": False,
    "enable_rfc8707": True,
    "enable_rfc9101": True,
    "enable_rfc9126": True,
    "enable_rfc9396": True,
    "enable_rfc9449": True,
    "enable_rfc9700": True,
    "enable_oidc_frontchannel_logout": True,
    "enable_oidc_backchannel_logout": True,
    "oauth21_alignment_mode": "tracked",
    "enable_rfc7800": False,
    "enable_rfc7952": False,
    "enable_rfc8291": False,
    "enable_rfc8812": False,
    "enable_rfc8932": False,
    "enable_rfc8523": False,
}

PROFILE_DEFAULT_OVERRIDES: Final[dict[str, dict[str, Any]]] = {
    "fapi2-security": {
        "enable_rfc8705": True,
        "enable_id_token_encryption": True,
        "require_tls": True,
        "strict_boundary_enforcement": True,
    },
}

SURFACE_SET_REGISTRY: Final[dict[str, dict[str, bool]]] = {
    "public-rest": {
        "surface_public_enabled": True,
        "surface_admin_enabled": False,
        "surface_rpc_enabled": False,
        "surface_diagnostics_enabled": False,
    },
    "admin-rpc": {
        "surface_public_enabled": False,
        "surface_admin_enabled": True,
        "surface_rpc_enabled": True,
        "surface_diagnostics_enabled": False,
    },
    "admin-rest": {
        "surface_public_enabled": False,
        "surface_admin_enabled": True,
        "surface_rpc_enabled": False,
        "surface_diagnostics_enabled": False,
    },
    "diagnostics": {
        "surface_public_enabled": False,
        "surface_admin_enabled": False,
        "surface_rpc_enabled": False,
        "surface_diagnostics_enabled": True,
    },
    "public-api": {
        "surface_public_enabled": True,
        "surface_admin_enabled": False,
        "surface_rpc_enabled": False,
        "surface_diagnostics_enabled": False,
    },
    "platform-admin-api": {
        "surface_public_enabled": False,
        "surface_admin_enabled": True,
        "surface_rpc_enabled": False,
        "surface_diagnostics_enabled": False,
    },
    "tenant-admin-api": {
        "surface_public_enabled": False,
        "surface_admin_enabled": True,
        "surface_rpc_enabled": True,
        "surface_diagnostics_enabled": False,
    },
    "developer-api": {
        "surface_public_enabled": True,
        "surface_admin_enabled": True,
        "surface_rpc_enabled": True,
        "surface_diagnostics_enabled": False,
    },
    "service-admin-api": {
        "surface_public_enabled": True,
        "surface_admin_enabled": True,
        "surface_rpc_enabled": True,
        "surface_diagnostics_enabled": False,
    },
    "resource-validation-api": {
        "surface_public_enabled": True,
        "surface_admin_enabled": False,
        "surface_rpc_enabled": False,
        "surface_diagnostics_enabled": False,
    },
    "my-account-api": {
        "surface_public_enabled": True,
        "surface_admin_enabled": False,
        "surface_rpc_enabled": False,
        "surface_diagnostics_enabled": False,
    },
}

PRODUCT_SURFACE_REGISTRY: Final[dict[str, dict[str, Any]]] = {
    "public-api": {
        "surface_sets": ("public-rest",),
        "allowed_capabilities": None,
        "admin_resources": (),
        "admin_rest_groups": (),
        "rpc_method_prefixes": (),
    },
    "platform-admin-api": {
        "surface_sets": ("admin-rest",),
        "allowed_capabilities": (),
        "admin_resources": (
            "Realm",
            "Tenant",
            "User",
            "AuditEvent",
            "KeyRotationEvent",
        ),
        "admin_rest_groups": ("admin_auth", "admin_realms"),
        "rpc_method_prefixes": (
            "audit.",
            "discovery.",
            "flow.",
            "identity.",
            "profile.",
            "rpc.",
            "target.",
            "tenant.",
        ),
    },
    "tenant-admin-api": {
        "surface_sets": ("admin-rpc",),
        "allowed_capabilities": (),
        "admin_resources": (
            "User",
            "Client",
            "ClientRegistration",
            "Consent",
            "AuditEvent",
            "KeyRotationEvent",
        ),
        "admin_rest_groups": ("admin_auth", "admin_identities"),
        "rpc_method_prefixes": (
            "audit.",
            "client.",
            "client.registration.",
            "consent.",
            "discovery.",
            "identity.",
            "jwks.",
            "keys.",
            "profile.",
            "rpc.",
            "target.",
            "tenant.keys.",
        ),
    },
    "developer-api": {
        "surface_sets": ("public-rest", "admin-rpc"),
        "allowed_capabilities": (
            "register",
            "register-management",
            "openid-configuration",
            "tenant-openid-configuration",
            "realm-openid-configuration",
            "oauth-authorization-server-metadata",
            "jwks",
            "tenant-jwks",
            "realm-jwks",
        ),
        "admin_resources": ("Client", "ClientRegistration", "AuditEvent"),
        "admin_rest_groups": (),
        "rpc_method_prefixes": (
            "client.",
            "client.registration.",
            "discovery.",
            "jwks.",
            "profile.",
            "rpc.",
            "target.",
        ),
    },
    "service-admin-api": {
        "surface_sets": ("public-rest", "admin-rpc"),
        "allowed_capabilities": (
            "introspection",
            "openid-configuration",
            "tenant-openid-configuration",
            "realm-openid-configuration",
            "oauth-protected-resource-metadata",
            "jwks",
            "tenant-jwks",
            "realm-jwks",
        ),
        "admin_resources": (
            "ApiKey",
            "Service",
            "ServiceKey",
            "TokenRecord",
            "AuditEvent",
        ),
        "admin_rest_groups": (),
        "rpc_method_prefixes": (
            "audit.",
            "discovery.",
            "jwks.",
            "keys.",
            "profile.",
            "rpc.",
            "target.",
            "token.",
        ),
    },
    "resource-validation-api": {
        "surface_sets": ("public-rest",),
        "allowed_capabilities": (
            "introspection",
            "openid-configuration",
            "tenant-openid-configuration",
            "realm-openid-configuration",
            "oauth-protected-resource-metadata",
            "jwks",
            "tenant-jwks",
            "realm-jwks",
        ),
        "admin_resources": (),
        "admin_rest_groups": (),
        "rpc_method_prefixes": (),
    },
    "my-account-api": {
        "surface_sets": ("public-rest",),
        "allowed_capabilities": (
            "openid-configuration",
            "tenant-openid-configuration",
            "realm-openid-configuration",
            "jwks",
            "tenant-jwks",
            "realm-jwks",
            "account-profile",
            "account-sessions",
            "account-consents",
            "account-credentials",
        ),
        "admin_resources": (),
        "admin_rest_groups": (),
        "rpc_method_prefixes": (),
    },
}

PLUGIN_MODE_TO_SURFACE_SETS: Final[dict[str, tuple[str, ...]]] = {
    "public-only": ("public-rest",),
    "admin-only": ("admin-rpc",),
    "mixed": ("public-rest", "admin-rpc", "diagnostics"),
    "diagnostics-only": ("diagnostics",),
}

PROTOCOL_SLICE_REGISTRY: Final[dict[str, dict[str, Any]]] = {
    "device": {
        "flags": ("enable_rfc8628",),
        "routes": ("/device_authorization",),
        "targets": ("RFC 8628",),
    },
    "token-exchange": {
        "flags": ("enable_rfc8693",),
        "routes": ("/token/exchange",),
        "targets": ("RFC 8693",),
    },
    "par": {
        "flags": ("enable_rfc9126",),
        "routes": ("/par",),
        "targets": ("RFC 9126",),
    },
    "jar": {
        "flags": ("enable_rfc9101",),
        "routes": (),
        "targets": ("RFC 9101",),
    },
    "rar": {
        "flags": ("enable_rfc9396",),
        "routes": (),
        "targets": ("RFC 9396",),
    },
    "dpop": {
        "flags": ("enable_rfc9449",),
        "routes": (),
        "targets": ("RFC 9449",),
    },
    "mtls": {
        "flags": ("enable_rfc8705",),
        "routes": (),
        "targets": ("RFC 8705",),
    },
}

EXTENSION_REGISTRY: Final[dict[str, dict[str, Any]]] = {
    "webauthn-passkeys": {
        "flags": ("enable_rfc8812",),
        "targets": ("RFC 8812",),
        "boundary": "extension_quarantine",
    },
    "set": {
        "flags": ("enable_rfc7952",),
        "targets": ("RFC 7952",),
        "boundary": "extension_quarantine",
    },
    "webpush": {
        "flags": ("enable_rfc8291",),
        "targets": ("RFC 8291",),
        "boundary": "extension_quarantine",
    },
    "dns-privacy": {
        "flags": ("enable_rfc8932",),
        "targets": ("RFC 8932",),
        "boundary": "extension_quarantine",
    },
}

SURFACE_CAPABILITY_REGISTRY: Final[dict[str, dict[str, Any]]] = (
    all_surface_capability_registry()
)
ROUTE_REGISTRY: Final[dict[str, dict[str, Any]]] = surface_route_registry()


OPENRPC_METHOD_REGISTRY: Final[dict[str, dict[str, Any]]] = get_rpc_method_registry()

TARGET_FLAG_REQUIREMENTS: Final[dict[str, tuple[str, ...]]] = {
    "RFC 6749": ("enable_rfc6749", "surface_public_enabled"),
    "RFC 6750": ("enable_rfc6750", "surface_public_enabled"),
    "RFC 7636": ("enable_rfc7636", "surface_public_enabled"),
    "RFC 8414": ("enable_rfc8414", "surface_public_enabled"),
    "RFC 8615": ("enable_rfc8615", "surface_public_enabled"),
    "RFC 7515": ("enable_rfc7515", "surface_public_enabled"),
    "RFC 7516": ("enable_rfc7516", "surface_public_enabled"),
    "RFC 7517": ("enable_rfc7517", "surface_public_enabled"),
    "RFC 7518": ("enable_rfc7518", "surface_public_enabled"),
    "RFC 7519": ("enable_rfc7519", "surface_public_enabled"),
    "RFC 7009": ("enable_rfc7009", "surface_public_enabled"),
    "RFC 7521": ("enable_rfc7521", "surface_public_enabled"),
    "RFC 7523": ("enable_rfc7523", "surface_public_enabled"),
    "RFC 7591": ("enable_rfc7591", "surface_public_enabled"),
    "RFC 7592": ("enable_rfc7592", "surface_public_enabled"),
    "RFC 7662": ("enable_rfc7662", "surface_public_enabled"),
    "RFC 8252": ("enable_rfc8252", "surface_public_enabled"),
    "RFC 8628": ("enable_rfc8628", "surface_public_enabled"),
    "RFC 8693": ("enable_rfc8693", "surface_public_enabled"),
    "RFC 8705": ("enable_rfc8705", "surface_public_enabled"),
    "RFC 8707": ("enable_rfc8707", "surface_public_enabled"),
    "RFC 9068": ("enable_rfc9068", "surface_public_enabled"),
    "RFC 9101": ("enable_rfc9101", "surface_public_enabled"),
    "RFC 9126": ("enable_rfc9126", "surface_public_enabled"),
    "RFC 9207": ("enable_rfc9207", "surface_public_enabled"),
    "RFC 9396": ("enable_rfc9396", "surface_public_enabled"),
    "RFC 9449": ("enable_rfc9449", "surface_public_enabled"),
    "RFC 9700": ("enable_rfc9700", "surface_public_enabled"),
    "RFC 9728": ("enable_rfc9728", "surface_public_enabled"),
    "RFC 6265": ("enable_oidc_session_management", "surface_public_enabled"),
    "OIDC Core 1.0": ("enable_oidc_core", "surface_public_enabled"),
    "OIDC Discovery 1.0": ("enable_oidc_discovery", "surface_public_enabled"),
    "OIDC UserInfo": ("enable_oidc_userinfo", "surface_public_enabled"),
    "OIDC Session Management": (
        "enable_oidc_session_management",
        "surface_public_enabled",
    ),
    "OIDC RP-Initiated Logout": (
        "enable_oidc_rp_initiated_logout",
        "surface_public_enabled",
    ),
    "OIDC Front-Channel Logout": (
        "enable_oidc_frontchannel_logout",
        "surface_public_enabled",
    ),
    "OIDC Back-Channel Logout": (
        "enable_oidc_backchannel_logout",
        "surface_public_enabled",
    ),
    "OpenAPI 3.1 / 3.2 compatible public contract": ("surface_public_enabled",),
    "OpenRPC 1.4.x admin/control-plane contract": (
        "surface_admin_enabled",
        "surface_rpc_enabled",
    ),
}


VALID_PROFILES: Final[tuple[str, ...]] = (
    "baseline",
    "baseline-development",
    "production",
    "hardening",
    "fapi2-security",
    "peer-claim",
)
VALID_PLUGIN_MODES: Final[tuple[str, ...]] = tuple(PLUGIN_MODE_TO_SURFACE_SETS)
VALID_RUNTIME_STYLES: Final[tuple[str, ...]] = ("plugin", "standalone")
VALID_PRODUCT_SURFACES: Final[tuple[str, ...]] = tuple(PRODUCT_SURFACE_REGISTRY)


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
    active_openrpc_methods: tuple[str, ...]
    product_surface: str | None = None
    allowed_admin_resources: tuple[str, ...] = ()
    allowed_admin_rest_groups: tuple[str, ...] = ()
    profile_source: dict[str, Any] = field(default_factory=dict)

    def flag_enabled(self, name: str) -> bool:
        return bool(self.flags.get(name, False))

    def surface_enabled(self, name: str) -> bool:
        if name in SURFACE_SET_REGISTRY:
            return name in self.surface_sets
        mapping = {
            "public-rest": "surface_public_enabled",
            "admin-rpc": "surface_admin_enabled",
            "admin-rest": "surface_admin_enabled",
            "diagnostics": "surface_diagnostics_enabled",
            "rpc": "surface_rpc_enabled",
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

    def method_enabled(self, name: str) -> bool:
        return name in self.active_openrpc_methods

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
            "active_openrpc_methods": list(self.active_openrpc_methods),
            "product_surface": self.product_surface,
            "allowed_admin_resources": list(self.allowed_admin_resources),
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


def _rpc_method_allowed(name: str, product_meta: dict[str, Any] | None) -> bool:
    if product_meta is None:
        return True
    exact = tuple(str(item) for item in product_meta.get("rpc_methods", ()))
    prefixes = tuple(str(item) for item in product_meta.get("rpc_method_prefixes", ()))
    return name in exact or any(name.startswith(prefix) for prefix in prefixes)


def _plugin_mode_for_surface_sets(surface_sets: tuple[str, ...]) -> str:
    surface_set = set(surface_sets)
    if surface_set == {"public-rest"}:
        return "public-only"
    if surface_set in ({"admin-rpc"}, {"admin-rest"}):
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
    if raw.get("surface_admin_enabled", True) or raw.get("surface_rpc_enabled", True):
        derived.append("admin-rpc")
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


def resolve_deployment(
    settings_obj: object | None = None,
    *,
    profile: str | None = None,
    surface_sets: tuple[str, ...] | list[str] | str | None = None,
    protocol_slices: tuple[str, ...] | list[str] | str | None = None,
    extensions: tuple[str, ...] | list[str] | str | None = None,
    plugin_mode: str | None = None,
    runtime_style: str | None = None,
    product_surface: str | None = None,
    flag_overrides: dict[str, Any] | None = None,
    profile_source: dict[str, Any] | None = None,
) -> ResolvedDeployment:
    raw = _settings_dict(settings_obj)
    if flag_overrides:
        raw.update(flag_overrides)

    profile_name = _valid_or_default(
        profile or str(raw.get("deployment_profile", "baseline")),
        VALID_PROFILES,
        "baseline",
    )
    raw.update(PROFILE_DEFAULT_OVERRIDES.get(profile_name, {}))
    plugin_mode_name = _valid_or_default(
        plugin_mode or str(raw.get("surface_plugin_mode", "mixed")),
        VALID_PLUGIN_MODES,
        "mixed",
    )
    runtime_style_name = _valid_or_default(
        runtime_style or str(raw.get("runtime_style", "standalone")),
        VALID_RUNTIME_STYLES,
        "standalone",
    )
    if plugin_mode is not None:
        raw["surface_plugin_mode"] = plugin_mode_name

    allowed_profile_flags = set(flags_for_profile(profile_name))
    requested_surface_sets = _csv_items(
        surface_sets if surface_sets is not None else raw.get("active_surface_sets")
    )
    requested_protocol_slices = _csv_items(
        protocol_slices
        if protocol_slices is not None
        else raw.get("active_protocol_slices")
    )
    requested_extensions = _csv_items(
        extensions if extensions is not None else raw.get("active_extensions")
    )

    product_surface_name = product_surface or next(
        (name for name in requested_surface_sets if name in PRODUCT_SURFACE_REGISTRY),
        None,
    )
    product_meta = _product_config(product_surface_name)
    if product_meta is not None:
        effective_surface_sets = tuple(
            str(item) for item in product_meta.get("surface_sets", ())
        )
        plugin_mode_name = _plugin_mode_for_surface_sets(effective_surface_sets)
        raw["surface_plugin_mode"] = plugin_mode_name
    else:
        effective_surface_sets = _derive_surface_sets(
            raw, plugin_mode_name, requested_surface_sets
        )
    effective_protocol_slices = _derive_protocol_slices(
        raw, allowed_profile_flags, requested_protocol_slices
    )
    effective_extensions = _derive_extensions(raw, requested_extensions)

    flags: dict[str, bool | str] = {}
    profile_flags = _all_profile_flags()
    for group_name, group in FEATURE_FLAG_GROUPS.items():
        group_flags = group.get("flags", {})
        if isinstance(group_flags, dict):
            names = tuple(group_flags.keys())
        else:
            names = tuple()
        for name in names:
            value = raw.get(name, DEFAULT_VALUES.get(name, False))
            if name in profile_flags:
                flags[name] = bool(value) and name in allowed_profile_flags
            elif name == "surface_plugin_mode":
                flags[name] = plugin_mode_name
            elif name == "oauth21_alignment_mode":
                flags[name] = str(value)
            else:
                flags[name] = bool(value) if isinstance(value, bool) else value

    for slice_name, meta in PROTOCOL_SLICE_REGISTRY.items():
        active = slice_name in effective_protocol_slices
        for flag in meta.get("flags", ()):
            flags[flag] = bool(flags.get(flag, False)) and active

    for extension_name, meta in EXTENSION_REGISTRY.items():
        active = extension_name in effective_extensions
        for flag in meta.get("flags", ()):
            if flag in flags:
                flags[flag] = bool(flags.get(flag, False)) and active

    surfaces = {
        "surface_public_enabled": "public-rest" in effective_surface_sets,
        "surface_admin_enabled": bool(
            {"admin-rest", "admin-rpc"}.intersection(effective_surface_sets)
        ),
        "surface_rpc_enabled": "admin-rpc" in effective_surface_sets,
        "surface_diagnostics_enabled": "diagnostics" in effective_surface_sets,
        "surface_operator_enabled": bool(raw.get("surface_operator_enabled", True)),
        "surface_plugin_mode": plugin_mode_name,
    }
    flags.update(surfaces)

    active_capabilities: list[str] = []
    active_routes: list[str] = []
    for capability_name, meta in SURFACE_CAPABILITY_REGISTRY.items():
        if meta.get("surface_set") not in effective_surface_sets:
            continue
        if not _capability_allowed(capability_name, product_meta):
            continue
        required_flags = tuple(meta.get("flags", ()))
        if all(bool(flags.get(name, False)) for name in required_flags):
            active_capabilities.append(capability_name)
            for path in tuple(meta.get("paths", ())):
                path_str = str(path)
                if path_str not in active_routes:
                    active_routes.append(path_str)

    active_contract_routes = [
        path
        for path in active_routes
        if bool(ROUTE_REGISTRY.get(path, {}).get("contract_visible", False))
    ]
    active_discovery_routes = [
        path
        for path in active_routes
        if bool(ROUTE_REGISTRY.get(path, {}).get("discovery_visible", False))
    ]

    active_targets: list[str] = []
    for label, required_flags in TARGET_FLAG_REQUIREMENTS.items():
        if all(bool(flags.get(name, False)) for name in required_flags):
            active_targets.append(label)

    if runtime_style_name in {"plugin", "standalone"}:
        active_targets.append("ASGI 3 application package")
    if runtime_style_name == "standalone":
        active_targets.extend(
            [
                "Runner profile: Uvicorn",
                "Runner profile: Hypercorn",
                "Runner profile: Tigrcorn",
            ]
        )
    if surfaces.get("surface_operator_enabled", False):
        active_targets.extend(
            [
                "CLI operator surface",
                "Bootstrap and migration lifecycle",
                "Key lifecycle and JWKS publication",
                "Import/export portability",
                "Release bundle and signature verification",
            ]
        )
    active_targets = list(dict.fromkeys(active_targets))

    active_methods: list[str] = []
    if bool(surfaces["surface_rpc_enabled"]):
        for name, meta in OPENRPC_METHOD_REGISTRY.items():
            if meta.get("surface_set") in effective_surface_sets:
                if not _rpc_method_allowed(name, product_meta):
                    continue
                active_methods.append(name)

    return ResolvedDeployment(
        profile=profile_name,
        plugin_mode=plugin_mode_name,
        runtime_style=runtime_style_name,
        surface_sets=tuple(effective_surface_sets),
        protocol_slices=tuple(effective_protocol_slices),
        extensions=tuple(effective_extensions),
        issuer=str(raw.get("issuer", DEFAULT_VALUES["issuer"])),
        protected_resource_identifier=str(
            raw.get(
                "protected_resource_identifier",
                DEFAULT_VALUES["protected_resource_identifier"],
            )
        ),
        strict_boundary_enforcement=bool(raw.get("strict_boundary_enforcement", True)),
        surfaces=surfaces,
        flags=flags,
        active_capabilities=tuple(active_capabilities),
        active_routes=tuple(active_routes),
        active_contract_routes=tuple(active_contract_routes),
        active_discovery_routes=tuple(active_discovery_routes),
        active_targets=tuple(active_targets),
        active_openrpc_methods=tuple(active_methods),
        product_surface=product_surface_name,
        allowed_admin_resources=tuple(
            str(item) for item in (product_meta or {}).get("admin_resources", ())
        ),
        allowed_admin_rest_groups=tuple(
            str(item) for item in (product_meta or {}).get("admin_rest_groups", ())
        ),
        profile_source=dict(
            profile_source
            or {"kind": "packaged-profile-id", "profile_id": profile_name}
        ),
    )


def deployment_from_app(
    app: Any | None, fallback_settings: object | None = None
) -> ResolvedDeployment:
    state = getattr(app, "state", None) if app is not None else None
    deployment = (
        getattr(state, "tigrbl_auth_deployment", None) if state is not None else None
    )
    if isinstance(deployment, ResolvedDeployment):
        return deployment
    return resolve_deployment(fallback_settings)


def deployment_from_request(
    request: Any | None, fallback_settings: object | None = None
) -> ResolvedDeployment:
    app = getattr(request, "app", None) if request is not None else None
    return deployment_from_app(app, fallback_settings)


__all__ = [
    "DEFAULT_VALUES",
    "EXTENSION_REGISTRY",
    "OPENRPC_METHOD_REGISTRY",
    "PLUGIN_MODE_TO_SURFACE_SETS",
    "PRODUCT_SURFACE_REGISTRY",
    "PROTOCOL_SLICE_REGISTRY",
    "ROUTE_REGISTRY",
    "ResolvedDeployment",
    "SURFACE_SET_REGISTRY",
    "TARGET_FLAG_REQUIREMENTS",
    "SURFACE_CAPABILITY_REGISTRY",
    "VALID_PLUGIN_MODES",
    "VALID_PRODUCT_SURFACES",
    "VALID_PROFILES",
    "VALID_RUNTIME_STYLES",
    "resolve_deployment",
    "deployment_from_app",
    "deployment_from_request",
]
