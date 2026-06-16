from __future__ import annotations

from .admin_routes import *
from .admin_routes import (
    _admin_table_resources,
    _attach_admin_security_metadata,
    _rewrite_admin_table_routes,
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


def build_surface_api(
    settings_obj: object | None = None,
    *,
    deployment: ResolvedDeployment | None = None,
) -> TigrblRouter:
    deployment = _as_deployment(settings_obj, deployment=deployment)
    router = TigrblRouter(engine=dsn)
    if deployment.flag_enabled("surface_admin_enabled"):
        if deployment.product_surface == "platform-admin-api":
            router.include_router(admin_realms_api)
            router.include_router(admin_tenants_api)
        admin_resources = _admin_table_resources(deployment)
        if admin_resources:
            if deployment.product_surface == "platform-admin-api":
                for resource in admin_resources:
                    if resource.__name__ in {"Realm", "Tenant"}:
                        continue
                    else:
                        router.include_table(resource)
            else:
                router.include_tables(admin_resources)
            _rewrite_admin_table_routes(router, deployment)
        for entry in ADMIN_ROUTER_BINDINGS:
            if deployment.admin_rest_group_enabled(str(entry["mount_group"])):
                router.include_router(entry["router"])
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
    return router


surface_api = build_surface_api()


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
    "ADMIN_ROUTER_BINDINGS",
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
