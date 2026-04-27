"""Executable release-path surface composition for Tigrbl-auth.

The capability identifiers used here must stay synchronized with
``tigrbl_auth.config.surfaces.PUBLIC_CAPABILITIES`` so deployment resolution,
runtime mounting, contract generation, and verification all observe the same
installed surface shape.
"""

from __future__ import annotations

from dataclasses import replace
from typing import Any, Callable, Final

from tigrbl_auth.framework import TigrblApp, TigrblRouter
from tigrbl_auth.api.rest.routers.authorize import api as authorize_api
from tigrbl_auth.api.rest.routers.device_authorization import api as device_authorization_api
from tigrbl_auth.api.rest.routers.login import api as login_api
from tigrbl_auth.api.rest.routers.logout import api as logout_api
from tigrbl_auth.api.rest.routers.par import api as par_api
from tigrbl_auth.api.rest.routers.register import api as register_api
from tigrbl_auth.api.rest.routers.revoke import api as revoke_api
from tigrbl_auth.api.rest.routers.token import api as token_api
from tigrbl_auth.config.deployment import ResolvedDeployment, resolve_deployment
from tigrbl_auth.standards.oidc.discovery import include_jwks, include_openid_configuration
from tigrbl_auth.standards.oidc.userinfo import include_oidc_userinfo
from tigrbl_auth.standards.oauth2.introspection import include_introspection_endpoint
from tigrbl_auth.standards.oauth2.rfc8414 import include_rfc8414
from tigrbl_auth.standards.oauth2.rfc9728 import include_rfc9728
from tigrbl_auth.standards.oauth2.token_exchange import include_token_exchange_endpoint
from tigrbl_auth.security.admin_gate import ADMIN_OPENAPI_SECURITY_DEPENDENCIES
from tigrbl_auth.tables import (
    ApiKey,
    AuditEvent,
    AuthCode,
    AuthSession,
    Client,
    ClientRegistration,
    Consent,
    KeyRotationEvent,
    LogoutState,
    PushedAuthorizationRequest,
    RevokedToken,
    Service,
    ServiceKey,
    Tenant,
    TokenRecord,
    User,
)
from tigrbl_auth.tables.engine import dsn

TABLE_RESOURCES = [
    Tenant,
    User,
    Client,
    ClientRegistration,
    ApiKey,
    Service,
    ServiceKey,
    AuthSession,
    AuthCode,
    TokenRecord,
    RevokedToken,
    Consent,
    LogoutState,
    KeyRotationEvent,
    AuditEvent,
    PushedAuthorizationRequest,
]


def admin_resource_path_prefixes() -> tuple[str, ...]:
    return tuple(f"/{resource.__name__.lower()}" for resource in TABLE_RESOURCES)


def _path_has_prefix(path: str, prefix: str) -> bool:
    return path == prefix or path.startswith(f"{prefix}/")


def _requires_admin_security_metadata(
    path: str,
    deployment: ResolvedDeployment,
    *,
    rpc_prefix: str,
    diagnostics_prefix: str,
) -> bool:
    if deployment.surface_enabled("admin-rpc") and any(
        _path_has_prefix(path, prefix) for prefix in admin_resource_path_prefixes()
    ):
        return True
    if deployment.flag_enabled("surface_rpc_enabled") and _path_has_prefix(path, rpc_prefix):
        return True
    if deployment.flag_enabled("surface_diagnostics_enabled") and _path_has_prefix(path, diagnostics_prefix):
        return True
    return False


def _attach_admin_security_metadata(
    router: TigrblRouter,
    deployment: ResolvedDeployment,
    *,
    rpc_prefix: str,
    diagnostics_prefix: str,
) -> None:
    secured_routes = []
    for route in getattr(router, "_routes", []):
        route_path = getattr(route, "path_template", None) or getattr(route, "path", "")
        if not _requires_admin_security_metadata(
            str(route_path),
            deployment,
            rpc_prefix=rpc_prefix,
            diagnostics_prefix=diagnostics_prefix,
        ):
            secured_routes.append(route)
            continue

        existing = list(getattr(route, "dependencies", None) or [])
        secured_routes.append(
            replace(
                route,
                dependencies=existing + list(ADMIN_OPENAPI_SECURITY_DEPENDENCIES),
            )
        )
    router._routes[:] = secured_routes

PUBLIC_ROUTER_BINDINGS: Final[tuple[dict[str, Any], ...]] = (
    {"mount_group": "login", "capabilities": ("login",), "router": login_api},
    {"mount_group": "authorize", "capabilities": ("authorize",), "router": authorize_api},
    {"mount_group": "token", "capabilities": ("token",), "router": token_api},
    {
        "mount_group": "register",
        "capabilities": ("register", "register-management"),
        "router": register_api,
    },
    {"mount_group": "revoke", "capabilities": ("revoke",), "router": revoke_api},
    {"mount_group": "logout", "capabilities": ("logout",), "router": logout_api},
    {
        "mount_group": "device_authorization",
        "capabilities": ("device-authorization",),
        "router": device_authorization_api,
    },
    {"mount_group": "par", "capabilities": ("par",), "router": par_api},
)

PUBLIC_PUBLISHER_BINDINGS: Final[tuple[dict[str, Any], ...]] = (
    {
        "mount_group": "userinfo",
        "capabilities": ("userinfo",),
        "include": include_oidc_userinfo,
    },
    {
        "mount_group": "introspection",
        "capabilities": ("introspection",),
        "include": include_introspection_endpoint,
    },
    {
        "mount_group": "token_exchange",
        "capabilities": ("token-exchange",),
        "include": include_token_exchange_endpoint,
    },
    {
        "mount_group": "oauth_protected_resource_metadata",
        "capabilities": ("oauth-protected-resource-metadata",),
        "include": include_rfc9728,
    },
    {
        "mount_group": "oauth_authorization_server_metadata",
        "capabilities": ("oauth-authorization-server-metadata",),
        "include": include_rfc8414,
    },
    {
        "mount_group": "openid_configuration",
        "capabilities": ("openid-configuration",),
        "include": include_openid_configuration,
    },
    {"mount_group": "jwks", "capabilities": ("jwks",), "include": include_jwks},
)


def _as_deployment(
    settings_obj: object | None = None,
    *,
    deployment: ResolvedDeployment | None = None,
) -> ResolvedDeployment:
    return deployment or resolve_deployment(settings_obj)


def build_surface_api(
    settings_obj: object | None = None,
    *,
    deployment: ResolvedDeployment | None = None,
) -> TigrblRouter:
    deployment = _as_deployment(settings_obj, deployment=deployment)
    router = TigrblRouter(engine=dsn)
    if deployment.surface_enabled("admin-rpc") or deployment.flag_enabled("surface_rpc_enabled"):
        router.include_tables(TABLE_RESOURCES)
    if deployment.surface_enabled("public-rest"):
        for entry in PUBLIC_ROUTER_BINDINGS:
            if any(deployment.capability_enabled(capability) for capability in entry["capabilities"]):
                router.include_router(entry["router"])
    return router


surface_api = build_surface_api()


def runtime_surface_binding_manifest() -> dict[str, Any]:
    return {
        "table_resources": [resource.__name__ for resource in TABLE_RESOURCES],
        "router_bindings": [
            {
                "mount_group": str(entry["mount_group"]),
                "capabilities": list(entry["capabilities"]),
                "router_module": getattr(entry["router"], "__module__", "unknown"),
            }
            for entry in PUBLIC_ROUTER_BINDINGS
        ],
        "publisher_bindings": [
            {
                "mount_group": str(entry["mount_group"]),
                "capabilities": list(entry["capabilities"]),
                "include_ref": f"{entry['include'].__module__}:{entry['include'].__name__}",
            }
            for entry in PUBLIC_PUBLISHER_BINDINGS
        ],
    }


def include_public_runtime_publishers(
    app: TigrblApp,
    settings_obj: object | None = None,
    *,
    deployment: ResolvedDeployment | None = None,
) -> None:
    deployment = _as_deployment(settings_obj, deployment=deployment)
    if not deployment.surface_enabled("public-rest"):
        return
    for entry in PUBLIC_PUBLISHER_BINDINGS:
        if any(deployment.capability_enabled(capability) for capability in entry["capabilities"]):
            include_fn: Callable[[TigrblApp], None] = entry["include"]
            include_fn(app)


def attach_runtime_surfaces(
    app: TigrblApp,
    settings_obj: object | None = None,
    *,
    deployment: ResolvedDeployment | None = None,
    rpc_prefix: str = "/rpc",
    diagnostics_prefix: str = "/system",
) -> TigrblRouter:
    deployment = _as_deployment(settings_obj, deployment=deployment)
    surface_router = build_surface_api(settings_obj, deployment=deployment)
    if deployment.flag_enabled("surface_rpc_enabled"):
        surface_router.mount_jsonrpc(prefix=rpc_prefix)
    if deployment.flag_enabled("surface_diagnostics_enabled"):
        surface_router.attach_diagnostics(prefix=diagnostics_prefix)
    _attach_admin_security_metadata(
        surface_router,
        deployment,
        rpc_prefix=rpc_prefix,
        diagnostics_prefix=diagnostics_prefix,
    )
    if any(
        bool(deployment.surfaces.get(key, False))
        for key in (
            "surface_public_enabled",
            "surface_admin_enabled",
            "surface_rpc_enabled",
            "surface_diagnostics_enabled",
        )
    ):
        app.include_router(surface_router)
    include_public_runtime_publishers(app, settings_obj, deployment=deployment)
    return surface_router


__all__ = [
    "TABLE_RESOURCES",
    "PUBLIC_ROUTER_BINDINGS",
    "PUBLIC_PUBLISHER_BINDINGS",
    "attach_runtime_surfaces",
    "admin_resource_path_prefixes",
    "build_surface_api",
    "include_public_runtime_publishers",
    "runtime_surface_binding_manifest",
    "surface_api",
]
