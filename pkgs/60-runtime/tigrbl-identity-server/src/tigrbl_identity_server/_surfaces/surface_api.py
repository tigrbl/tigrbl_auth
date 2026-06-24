from __future__ import annotations
# ruff: noqa: F403,F405

from typing import Any, Callable, Final

from tigrbl import TigrblApp, TigrblRouter
from tigrbl_identity_runtime.deployment import ResolvedDeployment, resolve_deployment
from tigrbl_identity_storage.tables.auth_code import api as authorize_api
from tigrbl_identity_storage.tables.auth_session import login_api
from tigrbl_identity_storage.tables.engine import dsn
from tigrbl_identity_storage.tables.token_record import api as token_api
from tigrbl_identity_storage_runtime.account_surface import api as my_account_api
from tigrbl_identity_storage_runtime.client_registration import include_client_registration_endpoint
from tigrbl_identity_storage_runtime.device_authorization import include_device_authorization_endpoint
from tigrbl_identity_storage_runtime.introspection import include_introspection_endpoint
from tigrbl_identity_storage_runtime.logout import include_logout_endpoint
from tigrbl_identity_storage_runtime.metadata.authorization_server_metadata import include_rfc8414
from tigrbl_identity_storage_runtime.metadata.oidc_discovery import include_jwks, include_openid_configuration
from tigrbl_identity_storage_runtime.metadata.protected_resource_metadata import include_rfc9728
from tigrbl_identity_storage_runtime.par import include_par_endpoint
from tigrbl_identity_storage_runtime.revocation import include_revocation_endpoint
from tigrbl_identity_storage_runtime.token_exchange import include_token_exchange_endpoint
from tigrbl_identity_storage_runtime.userinfo import include_oidc_userinfo

from .admin_routes import *
from .admin_routes import (
    _attach_admin_security_metadata,
    include_admin_routes,
)

PUBLIC_ROUTER_BINDINGS: Final[tuple[dict[str, Any], ...]] = (
    {
        "mount_group": "admin_auth",
        "capabilities": ("admin-auth",),
        "router": admin_auth_api,
    },
    {
        "mount_group": "admin_tenants",
        "capabilities": ("admin-auth",),
        "router": admin_tenants_api,
    },
    {
        "mount_group": "admin_identities",
        "capabilities": ("admin-auth",),
        "router": admin_identities_api,
    },
    {"mount_group": "login", "capabilities": ("login",), "router": login_api},
    {
        "mount_group": "authorize",
        "capabilities": ("authorize",),
        "router": authorize_api,
    },
    {"mount_group": "token", "capabilities": ("token",), "router": token_api},
    {
        "mount_group": "my_account",
        "capabilities": (
            "account-profile",
            "account-sessions",
            "account-consents",
            "account-credentials",
        ),
        "router": my_account_api,
    },
)

PUBLIC_PUBLISHER_BINDINGS: Final[tuple[dict[str, Any], ...]] = (
    {
        "mount_group": "register",
        "capabilities": ("register", "register-management"),
        "include": include_client_registration_endpoint,
    },
    {
        "mount_group": "logout",
        "capabilities": ("logout",),
        "include": include_logout_endpoint,
    },
    {
        "mount_group": "device_authorization",
        "capabilities": ("device-authorization",),
        "include": include_device_authorization_endpoint,
    },
    {
        "mount_group": "par",
        "capabilities": ("par",),
        "include": include_par_endpoint,
    },
    {
        "mount_group": "revoke",
        "capabilities": ("revoke",),
        "include": include_revocation_endpoint,
    },
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
        "capabilities": (
            "openid-configuration",
            "tenant-openid-configuration",
            "realm-openid-configuration",
        ),
        "include": include_openid_configuration,
    },
    {
        "mount_group": "jwks",
        "capabilities": ("jwks", "tenant-jwks", "realm-jwks"),
        "include": include_jwks,
    },
)


def _as_deployment(
    settings_obj: object | None = None,
    *,
    deployment: ResolvedDeployment | None = None,
) -> ResolvedDeployment:
    return deployment or resolve_deployment(settings_obj)


def build_public_router(
    settings_obj: object | None = None,
    *,
    deployment: ResolvedDeployment | None = None,
) -> TigrblRouter:
    deployment = _as_deployment(settings_obj, deployment=deployment)
    router = TigrblRouter(engine=dsn)
    selected_table_resources = include_admin_routes(router, deployment=deployment)
    if deployment.surface_enabled("public-rest"):
        for entry in PUBLIC_ROUTER_BINDINGS:
            if entry["router"] in {
                admin_auth_api,
                admin_realms_api,
                admin_tenants_api,
                admin_identities_api,
            }:
                continue
            if any(
                deployment.capability_enabled(capability)
                for capability in entry["capabilities"]
            ):
                router.include_router(entry["router"])
    assert_table_initialization_scope(deployment, selected_table_resources)
    return router


def build_surface_api(
    settings_obj: object | None = None,
    *,
    deployment: ResolvedDeployment | None = None,
) -> TigrblRouter:
    return build_public_router(settings_obj, deployment=deployment)


PublicRouter = build_public_router(deployment=resolve_deployment(plugin_mode="public-only"))
surface_api = PublicRouter


def runtime_surface_binding_manifest() -> dict[str, Any]:
    return {
        "table_resources": [resource.__name__ for resource in TABLE_RESOURCES],
        "admin_router_bindings": [
            {
                "mount_group": str(entry["mount_group"]),
                "router_module": getattr(entry["router"], "__module__", "unknown"),
            }
            for entry in ADMIN_ROUTER_BINDINGS
        ],
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
        if any(
            deployment.capability_enabled(capability)
            for capability in entry["capabilities"]
        ):
            include_fn: Callable[[TigrblApp], None] = entry["include"]
            include_fn(app)


def attach_runtime_surfaces(
    app: TigrblApp,
    settings_obj: object | None = None,
    *,
    deployment: ResolvedDeployment | None = None,
    diagnostics_prefix: str = "/system",
) -> TigrblRouter:
    deployment = _as_deployment(settings_obj, deployment=deployment)
    surface_router = build_surface_api(settings_obj, deployment=deployment)
    if deployment.flag_enabled("surface_diagnostics_enabled"):
        surface_router.attach_diagnostics(prefix=diagnostics_prefix)
    _attach_admin_security_metadata(
        surface_router,
        deployment,
        diagnostics_prefix=diagnostics_prefix,
    )
    if any(
        bool(deployment.surfaces.get(key, False))
        for key in (
            "surface_public_enabled",
            "surface_admin_enabled",
            "surface_diagnostics_enabled",
        )
    ):
        app.include_router(surface_router)
    include_public_runtime_publishers(app, settings_obj, deployment=deployment)
    return surface_router


__all__ = [
    "ADMIN_ROUTER_BINDINGS",
    "AdminRouter",
    "TABLE_RESOURCES",
    "TableInitializationScopeError",
    "PUBLIC_ROUTER_BINDINGS",
    "PUBLIC_PUBLISHER_BINDINGS",
    "assert_table_initialization_scope",
    "attach_runtime_surfaces",
    "admin_resource_path_prefixes",
    "build_admin_router",
    "build_public_router",
    "build_surface_api",
    "include_admin_routes",
    "include_public_runtime_publishers",
    "PublicRouter",
    "required_table_resource_names",
    "runtime_surface_binding_manifest",
    "surface_api",
    "table_initialization_manifest",
]
