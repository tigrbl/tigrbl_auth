"""Canonical executable surface capability registry.

This module is intentionally pure-data-first. Deployment resolution, runtime
mounting, contract generation, and modularity verification all consume the same
capability records so profile output is driven by executable surface wiring
rather than hand-maintained parallel route lists.
"""

from __future__ import annotations

from typing import Any, Final

PUBLIC_CAPABILITIES: Final[tuple[dict[str, Any], ...]] = (
    {
        "capability": "login",
        "kind": "router",
        "surface_set": "public-rest",
        "mount_group": "login",
        "paths": ("/login",),
        "methods": ("post",),
        "flags": ("enable_rfc6749",),
        "summary": "Password login helper",
        "tags": ("auth",),
        "router_ref": "tigrbl_auth.api.rest.routers.login:api",
        "targets": ("RFC 6749", "RFC 9068", "RFC 6265", "OIDC Session Management"),
        "contract_visible": True,
        "discovery_visible": False,
    },
    {
        "capability": "authorize",
        "kind": "router",
        "surface_set": "public-rest",
        "mount_group": "authorize",
        "paths": ("/authorize",),
        "methods": ("get",),
        "flags": ("enable_rfc6749", "enable_oidc_core"),
        "summary": "Authorization endpoint",
        "tags": ("oauth2", "oidc"),
        "router_ref": "tigrbl_auth.api.rest.routers.authorize:api",
        "targets": (
            "RFC 6749",
            "OIDC Core 1.0",
            "RFC 8252",
            "RFC 8707",
            "RFC 9101",
            "RFC 9207",
            "RFC 9396",
            "RFC 9700",
            "RFC 6265",
            "OIDC Session Management",
        ),
        "contract_visible": True,
        "discovery_visible": False,
    },
    {
        "capability": "token",
        "kind": "router",
        "surface_set": "public-rest",
        "mount_group": "token",
        "paths": ("/token",),
        "methods": ("post",),
        "flags": ("enable_rfc6749",),
        "summary": "Token endpoint",
        "tags": ("oauth2",),
        "router_ref": "tigrbl_auth.api.rest.routers.token:api",
        "targets": ("RFC 6749", "RFC 6750", "RFC 9068", "RFC 9700"),
        "contract_visible": True,
        "discovery_visible": False,
    },
    {
        "capability": "userinfo",
        "kind": "publisher",
        "surface_set": "public-rest",
        "mount_group": "userinfo",
        "paths": ("/userinfo",),
        "methods": ("get",),
        "flags": ("enable_oidc_userinfo",),
        "summary": "OIDC UserInfo endpoint",
        "tags": ("oidc",),
        "publisher_ref": "tigrbl_auth.standards.oidc.userinfo:include_oidc_userinfo",
        "targets": ("OIDC UserInfo", "RFC 6750"),
        "contract_visible": True,
        "discovery_visible": True,
    },
    {
        "capability": "introspection",
        "kind": "publisher",
        "surface_set": "public-rest",
        "mount_group": "introspection",
        "paths": ("/introspect",),
        "methods": ("post",),
        "flags": ("enable_rfc7662",),
        "summary": "Token introspection endpoint",
        "tags": ("oauth2",),
        "publisher_ref": "tigrbl_auth.standards.oauth2.introspection:include_introspection_endpoint",
        "targets": ("RFC 7662", "RFC 6750"),
        "contract_visible": True,
        "discovery_visible": True,
    },
    {
        "capability": "register",
        "kind": "router",
        "surface_set": "public-rest",
        "mount_group": "register",
        "paths": ("/register",),
        "methods": ("post",),
        "flags": ("enable_rfc7591",),
        "summary": "Dynamic client registration endpoint",
        "tags": ("oauth2",),
        "router_ref": "tigrbl_auth.api.rest.routers.register:api",
        "targets": ("RFC 7591", "RFC 8252", "OIDC RP-Initiated Logout"),
        "contract_visible": True,
        "discovery_visible": True,
    },
    {
        "capability": "register-management",
        "kind": "router",
        "surface_set": "public-rest",
        "mount_group": "register",
        "paths": ("/register/{client_id}",),
        "methods": ("get", "put", "delete"),
        "flags": ("enable_rfc7592",),
        "summary": "Dynamic client registration management endpoint",
        "tags": ("oauth2",),
        "router_ref": "tigrbl_auth.api.rest.routers.register:api",
        "targets": ("RFC 7592", "RFC 8252", "OIDC RP-Initiated Logout"),
        "contract_visible": True,
        "discovery_visible": False,
    },
    {
        "capability": "revoke",
        "kind": "router",
        "surface_set": "public-rest",
        "mount_group": "revoke",
        "paths": ("/revoke",),
        "methods": ("post",),
        "flags": ("enable_rfc7009",),
        "summary": "Token revocation endpoint",
        "tags": ("oauth2",),
        "router_ref": "tigrbl_auth.api.rest.routers.revoke:api",
        "targets": ("RFC 7009",),
        "contract_visible": True,
        "discovery_visible": True,
    },
    {
        "capability": "logout",
        "kind": "router",
        "surface_set": "public-rest",
        "mount_group": "logout",
        "paths": ("/logout",),
        "methods": ("get", "post"),
        "flags": ("enable_oidc_rp_initiated_logout",),
        "summary": "OIDC RP-initiated logout endpoint",
        "tags": ("oidc",),
        "router_ref": "tigrbl_auth.api.rest.routers.logout:api",
        "targets": (
            "RFC 6265",
            "OIDC Session Management",
            "OIDC RP-Initiated Logout",
            "OIDC Front-Channel Logout",
            "OIDC Back-Channel Logout",
        ),
        "contract_visible": True,
        "discovery_visible": True,
    },
    {
        "capability": "device-authorization",
        "kind": "router",
        "surface_set": "public-rest",
        "mount_group": "device_authorization",
        "paths": ("/device_authorization",),
        "methods": ("post",),
        "flags": ("enable_rfc8628",),
        "summary": "Device authorization endpoint",
        "tags": ("oauth2",),
        "router_ref": "tigrbl_auth.api.rest.routers.device_authorization:api",
        "targets": ("RFC 8628", "RFC 8707"),
        "contract_visible": True,
        "discovery_visible": True,
    },
    {
        "capability": "par",
        "kind": "router",
        "surface_set": "public-rest",
        "mount_group": "par",
        "paths": ("/par",),
        "methods": ("post",),
        "flags": ("enable_rfc9126",),
        "summary": "Pushed authorization request endpoint",
        "tags": ("oauth2",),
        "router_ref": "tigrbl_auth.api.rest.routers.par:api",
        "targets": ("RFC 9126", "RFC 9101", "RFC 9396", "RFC 8707", "RFC 9700"),
        "contract_visible": True,
        "discovery_visible": True,
    },
    {
        "capability": "token-exchange",
        "kind": "publisher",
        "surface_set": "public-rest",
        "mount_group": "token_exchange",
        "paths": ("/token/exchange",),
        "methods": ("post",),
        "flags": ("enable_rfc8693",),
        "summary": "Token exchange endpoint",
        "tags": ("oauth2",),
        "publisher_ref": "tigrbl_auth.standards.oauth2.token_exchange:include_token_exchange_endpoint",
        "targets": ("RFC 8693", "RFC 8705", "RFC 8707", "RFC 9068", "RFC 9449"),
        "contract_visible": True,
        "discovery_visible": False,
    },
    {
        "capability": "openid-configuration",
        "kind": "publisher",
        "surface_set": "public-rest",
        "mount_group": "openid_configuration",
        "paths": ("/.well-known/openid-configuration",),
        "methods": ("get",),
        "flags": ("enable_oidc_discovery", "enable_rfc8615"),
        "summary": "OIDC discovery document",
        "tags": (".well-known",),
        "publisher_ref": "tigrbl_auth.standards.oidc.discovery:include_openid_configuration",
        "artifact_name": "openid-configuration.json",
        "targets": ("OIDC Discovery 1.0", "RFC 8615", "RFC 9700"),
        "contract_visible": True,
        "discovery_visible": True,
    },
    {
        "capability": "tenant-openid-configuration",
        "kind": "publisher",
        "surface_set": "public-rest",
        "mount_group": "openid_configuration",
        "paths": ("/tenants/{tenant_slug}/.well-known/openid-configuration",),
        "methods": ("get",),
        "flags": ("enable_oidc_discovery", "enable_rfc8615"),
        "summary": "Tenant-scoped OIDC discovery document",
        "tags": (".well-known", "tenant"),
        "publisher_ref": "tigrbl_auth.standards.oidc.discovery:include_openid_configuration",
        "artifact_name": "tenant-openid-configuration.json",
        "targets": ("OIDC Discovery 1.0", "RFC 8615", "RFC 9700"),
        "contract_visible": True,
        "discovery_visible": True,
    },
    {
        "capability": "oauth-authorization-server-metadata",
        "kind": "publisher",
        "surface_set": "public-rest",
        "mount_group": "oauth_authorization_server_metadata",
        "paths": ("/.well-known/oauth-authorization-server",),
        "methods": ("get",),
        "flags": ("enable_rfc8414", "enable_rfc8615"),
        "summary": "OAuth authorization server metadata",
        "tags": (".well-known",),
        "publisher_ref": "tigrbl_auth.standards.oauth2.rfc8414:include_rfc8414",
        "artifact_name": "oauth-authorization-server.json",
        "targets": ("RFC 8414", "RFC 8615"),
        "contract_visible": True,
        "discovery_visible": True,
    },
    {
        "capability": "oauth-protected-resource-metadata",
        "kind": "publisher",
        "surface_set": "public-rest",
        "mount_group": "oauth_protected_resource_metadata",
        "paths": ("/.well-known/oauth-protected-resource",),
        "methods": ("get",),
        "flags": ("enable_rfc9728", "enable_rfc8615"),
        "summary": "OAuth protected resource metadata",
        "tags": (".well-known",),
        "publisher_ref": "tigrbl_auth.standards.oauth2.rfc9728:include_rfc9728",
        "artifact_name": "oauth-protected-resource.json",
        "targets": ("RFC 9728", "RFC 8615"),
        "contract_visible": True,
        "discovery_visible": True,
    },
    {
        "capability": "jwks",
        "kind": "publisher",
        "surface_set": "public-rest",
        "mount_group": "jwks",
        "paths": ("/.well-known/jwks.json",),
        "methods": ("get",),
        "flags": ("enable_rfc7517", "enable_rfc8615"),
        "summary": "JSON Web Key Set",
        "tags": (".well-known",),
        "publisher_ref": "tigrbl_auth.standards.oidc.discovery:include_jwks",
        "artifact_name": "jwks.json",
        "targets": ("RFC 7517", "RFC 8615"),
        "contract_visible": True,
        "discovery_visible": True,
    },
    {
        "capability": "tenant-jwks",
        "kind": "publisher",
        "surface_set": "public-rest",
        "mount_group": "jwks",
        "paths": ("/tenants/{tenant_slug}/.well-known/jwks.json",),
        "methods": ("get",),
        "flags": ("enable_rfc7517", "enable_rfc8615"),
        "summary": "Tenant-scoped JSON Web Key Set",
        "tags": (".well-known", "tenant"),
        "publisher_ref": "tigrbl_auth.standards.oidc.discovery:include_jwks",
        "artifact_name": "tenant-jwks.json",
        "targets": ("RFC 7517", "RFC 8615"),
        "contract_visible": True,
        "discovery_visible": True,
    },
)

DIAGNOSTICS_CAPABILITIES: Final[tuple[dict[str, Any], ...]] = (
    {
        "capability": "diagnostics-health",
        "kind": "diagnostics",
        "surface_set": "diagnostics",
        "mount_group": "diagnostics",
        "paths": ("/system/health",),
        "methods": ("get",),
        "flags": (),
        "summary": "Diagnostics health endpoint",
        "tags": ("diagnostics",),
        "contract_visible": False,
        "discovery_visible": False,
    },
)

ALL_SURFACE_CAPABILITIES: Final[tuple[dict[str, Any], ...]] = PUBLIC_CAPABILITIES + DIAGNOSTICS_CAPABILITIES


def public_capability_registry() -> dict[str, dict[str, Any]]:
    return {str(item["capability"]): dict(item) for item in PUBLIC_CAPABILITIES}


def diagnostics_capability_registry() -> dict[str, dict[str, Any]]:
    return {str(item["capability"]): dict(item) for item in DIAGNOSTICS_CAPABILITIES}


def all_surface_capability_registry() -> dict[str, dict[str, Any]]:
    return {str(item["capability"]): dict(item) for item in ALL_SURFACE_CAPABILITIES}


def capability_mount_groups() -> dict[str, list[str]]:
    groups: dict[str, list[str]] = {}
    for item in ALL_SURFACE_CAPABILITIES:
        groups.setdefault(str(item.get("mount_group", "default")), []).append(str(item["capability"]))
    return groups


def route_registry() -> dict[str, dict[str, Any]]:
    registry: dict[str, dict[str, Any]] = {}
    for item in ALL_SURFACE_CAPABILITIES:
        for path in item.get("paths", ()):  # type: ignore[union-attr]
            registry[str(path)] = {
                "surface_set": item.get("surface_set"),
                "methods": tuple(str(method) for method in item.get("methods", ())),
                "flags": tuple(str(flag) for flag in item.get("flags", ())),
                "summary": item.get("summary", str(path)),
                "tags": tuple(str(tag) for tag in item.get("tags", ())),
                "capability": item.get("capability"),
                "kind": item.get("kind"),
                "mount_group": item.get("mount_group"),
                "contract_visible": bool(item.get("contract_visible", True)),
                "discovery_visible": bool(item.get("discovery_visible", False)),
                "router_ref": item.get("router_ref"),
                "publisher_ref": item.get("publisher_ref"),
                "artifact_name": item.get("artifact_name"),
                "targets": tuple(str(target) for target in item.get("targets", ())),
            }
    return registry


def public_contract_paths() -> list[str]:
    paths: list[str] = []
    for item in PUBLIC_CAPABILITIES:
        if not bool(item.get("contract_visible", True)):
            continue
        for path in item.get("paths", ()):  # type: ignore[union-attr]
            if str(path) not in paths:
                paths.append(str(path))
    return paths


SURFACE_REGISTRY: dict[str, dict[str, Any]] = {
    "public_auth_plane": {
        "settings_flag": "surface_public_enabled",
        "surface_set": "public-rest",
        "capability_registry": "tigrbl_auth.config.surfaces.PUBLIC_CAPABILITIES",
        "current_routes": public_contract_paths(),
        "target_routes": public_contract_paths(),
    },
    "admin_control_plane": {
        "settings_flag": "surface_admin_enabled",
        "surface_set": "admin-rpc",
        "current_resources": [
            "Tenant",
            "User",
            "Client",
            "ClientRegistration",
            "ApiKey",
            "Service",
            "ServiceKey",
            "AuthSession",
            "AuthCode",
            "TokenRecord",
            "PushedAuthorizationRequest",
            "RevokedToken",
            "Consent",
            "LogoutState",
            "AuditEvent",
            "KeyRotationEvent",
        ],
        "target_resources": [
            "Tenant",
            "User",
            "Client",
            "ClientRegistration",
            "ApiKey",
            "Service",
            "ServiceKey",
            "AuthSession",
            "AuthCode",
            "TokenRecord",
            "PushedAuthorizationRequest",
            "RevokedToken",
            "Consent",
            "LogoutState",
            "AuditEvent",
            "KeyRotationEvent",
        ],
    },
    "operator_plane": {
        "settings_flag": "surface_operator_enabled",
        "current_commands": [
            "serve",
            "bootstrap",
            "migrate",
            "verify",
            "gate",
            "spec",
            "claims",
            "evidence",
            "adr",
            "doctor",
            "release",
            "tenant",
            "client",
            "identity",
            "flow",
            "session",
            "token",
            "keys",
            "discovery",
            "import",
            "export",
        ],
        "target_commands": [
            "bootstrap",
            "migrate",
            "serve",
            "verify",
            "gate",
            "spec",
            "evidence",
            "claims",
            "adr",
            "doctor",
            "release",
            "tenant",
            "client",
            "identity",
            "flow",
            "session",
            "token",
            "keys",
            "discovery",
            "import",
            "export",
        ],
    },
    "rpc_control_plane": {
        "settings_flag": "surface_rpc_enabled",
        "surface_set": "admin-rpc",
        "current_prefix": "/rpc",
        "target_prefix": "/rpc",
        "required_method": "rpc.discover",
    },
    "diagnostics_plane": {
        "settings_flag": "surface_diagnostics_enabled",
        "current_prefix": "/system",
        "target_prefix": "/system",
    },
    "plugin_plane": {
        "settings_flag": "surface_plugin_mode",
        "current_modes": ["mixed"],
        "target_modes": ["public-only", "admin-only", "mixed", "diagnostics-only"],
    },
}


def enabled_surface_summary(settings_obj: object) -> dict[str, bool | str]:
    from .deployment import resolve_deployment

    deployment = resolve_deployment(settings_obj)
    return dict(deployment.surfaces)


def surface_registry() -> dict[str, dict[str, Any]]:
    return SURFACE_REGISTRY


def surface_set_registry() -> dict[str, dict[str, bool]]:
    from .deployment import SURFACE_SET_REGISTRY

    return SURFACE_SET_REGISTRY


__all__ = [
    "ALL_SURFACE_CAPABILITIES",
    "DIAGNOSTICS_CAPABILITIES",
    "PUBLIC_CAPABILITIES",
    "SURFACE_REGISTRY",
    "all_surface_capability_registry",
    "capability_mount_groups",
    "diagnostics_capability_registry",
    "enabled_surface_summary",
    "public_capability_registry",
    "public_contract_paths",
    "route_registry",
    "surface_registry",
    "surface_set_registry",
]
