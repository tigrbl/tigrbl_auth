"""Executable release-path surface composition for Tigrbl-auth.

The capability identifiers used here must stay synchronized with
``tigrbl_auth.config.surfaces.PUBLIC_CAPABILITIES`` so deployment resolution,
runtime mounting, contract generation, and verification all observe the same
installed surface shape.
"""

from __future__ import annotations

from dataclasses import replace
import re
from typing import Any, Callable, Final

from tigrbl_auth.framework import TigrblApp, TigrblRouter
from tigrbl_auth.api.rest.routers.authorize import api as authorize_api
from tigrbl_auth.api.rest.routers.admin_auth import api as admin_auth_api
from tigrbl_auth.api.rest.routers.admin_identities import api as admin_identities_api
from tigrbl_auth.api.rest.routers.admin_tenants import api as admin_tenants_api
from tigrbl_auth.api.rest.routers.device_authorization import (
    api as device_authorization_api,
)
from tigrbl_auth.api.rest.routers.login import api as login_api
from tigrbl_auth.api.rest.routers.logout import api as logout_api
from tigrbl_auth.api.rest.routers.my_account import api as my_account_api
from tigrbl_auth.api.rest.routers.par import api as par_api
from tigrbl_auth.api.rest.routers.register import api as register_api
from tigrbl_auth.api.rest.routers.revoke import api as revoke_api
from tigrbl_auth.api.rest.routers.token import api as token_api
from tigrbl_auth.config.deployment import ResolvedDeployment, resolve_deployment
from tigrbl_auth.standards.oidc.discovery import (
    include_jwks,
    include_openid_configuration,
)
from tigrbl_auth.standards.oidc.userinfo import include_oidc_userinfo
from tigrbl_auth.standards.oauth2.introspection import include_introspection_endpoint
from tigrbl_auth.standards.oauth2.rfc8414 import include_rfc8414
from tigrbl_auth.standards.oauth2.rfc9728 import include_rfc9728
from tigrbl_auth.standards.oauth2.token_exchange import include_token_exchange_endpoint
from tigrbl_auth.security.admin_gate import ADMIN_OPENAPI_SECURITY_DEPENDENCIES
from tigrbl_auth._identity_storage import ensure_identity_storage_importable

ensure_identity_storage_importable()

from tigrbl_identity_storage.tables import (
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
from tigrbl_identity_storage.tables.engine import dsn

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

ADMIN_ROUTER_BINDINGS: Final[tuple[dict[str, Any], ...]] = (
    {"mount_group": "admin_auth", "router": admin_auth_api},
    {"mount_group": "admin_tenants", "router": admin_tenants_api},
    {"mount_group": "admin_identities", "router": admin_identities_api},
)


def _admin_table_resources(
    deployment: ResolvedDeployment | None = None,
) -> tuple[type[Any], ...]:
    if deployment is None or getattr(deployment, "product_surface", None) is None:
        return tuple(TABLE_RESOURCES)
    return tuple(
        resource
        for resource in TABLE_RESOURCES
        if deployment.admin_resource_enabled(resource.__name__)
    )


def _admin_resource_path(resource: type[Any], deployment: ResolvedDeployment | None = None) -> str:
    if getattr(deployment, "product_surface", None) == "platform-admin-api":
        if resource.__name__ == "Tenant":
            return "/admin/tenant"
        if resource.__name__ == "User":
            return "/admin/identity"
    return f"/{resource.__name__.lower()}"


def admin_resource_path_prefixes(
    deployment: ResolvedDeployment | None = None,
) -> tuple[str, ...]:
    return tuple(
        _admin_resource_path(resource, deployment)
        for resource in _admin_table_resources(deployment)
    )


def _path_has_prefix(path: str, prefix: str) -> bool:
    return path == prefix or path.startswith(f"{prefix}/")


def _requires_admin_security_metadata(
    path: str,
    deployment: ResolvedDeployment,
    *,
    rpc_prefix: str,
    diagnostics_prefix: str,
) -> bool:
    if deployment.flag_enabled("surface_admin_enabled") and any(
        _path_has_prefix(path, prefix)
        for prefix in admin_resource_path_prefixes(deployment)
    ):
        return True
    if deployment.flag_enabled("surface_rpc_enabled") and _path_has_prefix(
        path, rpc_prefix
    ):
        return True
    if deployment.flag_enabled("surface_diagnostics_enabled") and _path_has_prefix(
        path, diagnostics_prefix
    ):
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


def _route_pattern(path_template: str, param_names: tuple[str, ...]) -> re.Pattern[str]:
    pattern = re.escape(path_template)
    for name in param_names:
        pattern = pattern.replace(r"\{" + name + r"\}", f"(?P<{name}>[^/]+)")
    return re.compile(f"^{pattern}/?$")


def _rewrite_model_rest_bindings(
    model: type[Any],
    *,
    old_prefix: str,
    new_prefix: str,
) -> None:
    ops = getattr(model, "ops", None)
    by_alias = getattr(ops, "by_alias", None)
    if not isinstance(by_alias, dict):
        return

    for alias, specs in list(by_alias.items()):
        rewritten_specs = []
        changed = False
        for spec in tuple(specs or ()):
            next_bindings = []
            spec_changed = False
            for binding in tuple(getattr(spec, "bindings", ()) or ()):
                path = getattr(binding, "path", None)
                if isinstance(path, str) and path.startswith(old_prefix):
                    next_path = f"{new_prefix}{path[len(old_prefix):]}"
                    next_bindings.append(replace(binding, path=next_path))
                    spec_changed = True
                else:
                    next_bindings.append(binding)
            if spec_changed:
                rewritten_specs.append(
                    replace(spec, bindings=tuple(next_bindings))
                )
                changed = True
            else:
                rewritten_specs.append(spec)
        if changed:
            try:
                by_alias[alias] = type(specs)(tuple(rewritten_specs))
            except TypeError:
                by_alias[alias] = tuple(rewritten_specs)


def _rewrite_admin_table_routes(
    router: TigrblRouter,
    deployment: ResolvedDeployment,
) -> None:
    if deployment.product_surface != "platform-admin-api":
        return
    rewrites = {
        "Tenant": ("/tenant", "/admin/tenant"),
        "User": ("/user", "/admin/identity"),
    }
    for resource in _admin_table_resources(deployment):
        rewrite = rewrites.get(resource.__name__)
        if rewrite is not None:
            old_prefix, new_prefix = rewrite
            _rewrite_model_rest_bindings(
                resource,
                old_prefix=old_prefix,
                new_prefix=new_prefix,
            )
    rewritten = []
    for route in getattr(router, "_routes", []):
        model = getattr(route, "tigrbl_model", None)
        resource_name = getattr(model, "__name__", "")
        rewrite = rewrites.get(resource_name)
        path_template = str(getattr(route, "path_template", "") or "")
        if rewrite is None or not path_template.startswith(rewrite[0]):
            rewritten.append(route)
            continue
        old_prefix, new_prefix = rewrite
        next_path = f"{new_prefix}{path_template[len(old_prefix):]}"
        binding = getattr(route, "tigrbl_binding", None)
        if binding is not None and hasattr(binding, "path"):
            binding = replace(binding, path=next_path)
        _rewrite_model_rest_bindings(
            model,
            old_prefix=old_prefix,
            new_prefix=new_prefix,
        )
        rewritten.append(
            replace(
                route,
                path_template=next_path,
                pattern=_route_pattern(
                    next_path, tuple(getattr(route, "param_names", ()) or ())
                ),
                tigrbl_binding=binding,
            )
        )
    router._routes[:] = rewritten


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
    if deployment.flag_enabled("surface_admin_enabled"):
        if deployment.product_surface == "platform-admin-api":
            router.include_router(admin_tenants_api)
        admin_resources = _admin_table_resources(deployment)
        if admin_resources:
            if deployment.product_surface == "platform-admin-api":
                for resource in admin_resources:
                    if resource.__name__ == "Tenant":
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
