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

from tigrbl import TigrblApp, TigrblRouter
from tigrbl_identity_storage.tables.auth_code import api as authorize_api
from tigrbl_identity_storage.tables.auth_session import login_api
from tigrbl_identity_storage.tables.user._account_surface import api as my_account_api
from tigrbl_identity_storage.tables.client_registration import api as register_api
from tigrbl_identity_storage.tables.device_code import api as device_authorization_api
from tigrbl_identity_storage.tables.logout_state import api as logout_api
from tigrbl_identity_storage.tables.pushed_authorization_request import api as par_api
from tigrbl_identity_storage.tables.revoked_token import api as revoke_api
from tigrbl_identity_storage.tables.token_record import api as token_api
from tigrbl_identity_storage.tables.user import admin_api as admin_auth_api
from tigrbl_identity_storage.tables.user import admin_api as admin_identities_api
from tigrbl_identity_storage.tables.realm import admin_api as admin_realms_api
from tigrbl_identity_storage.tables.tenant import admin_api as admin_tenants_api
from tigrbl_identity_runtime.deployment import ResolvedDeployment, resolve_deployment
from tigrbl_identity_storage.tables.realm._oidc_discovery import (
    include_jwks,
    include_openid_configuration,
)
from tigrbl_identity_storage.tables.user._oidc_userinfo import include_oidc_userinfo
from tigrbl_identity_storage.tables.realm._oauth_authorization_server_metadata import include_rfc8414
from tigrbl_identity_storage.tables.token_record._introspection import include_introspection_endpoint
from tigrbl_identity_storage.tables.token_record._protected_resource_metadata import include_rfc9728
from tigrbl_identity_storage.tables.token_record._token_exchange import include_token_exchange_endpoint
from tigrbl_authz_policy_admin_gate import ADMIN_OPENAPI_SECURITY_DEPENDENCIES
from tigrbl_identity_storage import ensure_identity_storage_importable

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
    Realm,
    RevokedToken,
    Service,
    ServiceKey,
    Tenant,
    TokenRecord,
    User,
)
from tigrbl_identity_storage.tables.engine import dsn

TABLE_RESOURCES = [
    Realm,
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
    {"mount_group": "admin_realms", "router": admin_realms_api},
    {"mount_group": "admin_tenants", "router": admin_tenants_api},
    {"mount_group": "admin_identities", "router": admin_identities_api},
)


class TableInitializationScopeError(ValueError):
    """Raised when a product surface selects table resources outside its contract."""


def _admin_table_resources(
    deployment: ResolvedDeployment | None = None,
) -> tuple[type[Any], ...]:
    if deployment is None or getattr(deployment, "product_surface", None) is None:
        return tuple(TABLE_RESOURCES)
    required = getattr(deployment, "required_table_resources", ())
    if required:
        resources_by_name = {resource.__name__: resource for resource in TABLE_RESOURCES}
        return tuple(
            resources_by_name[name]
            for name in tuple(str(item) for item in required)
            if name in resources_by_name
        )
    return tuple(
        resource
        for resource in TABLE_RESOURCES
        if deployment.admin_resource_enabled(resource.__name__)
    )


def _resource_name(resource: type[Any] | str) -> str:
    return resource if isinstance(resource, str) else resource.__name__


def required_table_resource_names(
    deployment: ResolvedDeployment | None = None,
) -> tuple[str, ...]:
    return tuple(resource.__name__ for resource in _admin_table_resources(deployment))


def table_initialization_manifest(
    deployment: ResolvedDeployment | None = None,
) -> dict[str, Any]:
    return {
        "product_surface": getattr(deployment, "product_surface", None),
        "required_table_resources": list(required_table_resource_names(deployment)),
    }


def assert_table_initialization_scope(
    deployment: ResolvedDeployment,
    selected_resources: tuple[type[Any] | str, ...],
) -> None:
    if deployment.product_surface is None:
        return
    expected = set(required_table_resource_names(deployment))
    selected = set(_resource_name(resource) for resource in selected_resources)
    unexpected = sorted(selected - expected)
    missing = sorted(expected - selected)
    if unexpected or missing:
        raise TableInitializationScopeError(
            "product surface table initialization mismatch: "
            f"unexpected={unexpected}, missing={missing}"
        )


def _admin_resource_path(resource: type[Any], deployment: ResolvedDeployment | None = None) -> str:
    if getattr(deployment, "product_surface", None) == "platform-admin-api":
        if resource.__name__ == "Realm":
            return "/admin/realm"
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
    diagnostics_prefix: str,
) -> bool:
    if deployment.flag_enabled("surface_admin_enabled") and any(
        _path_has_prefix(path, prefix)
        for prefix in admin_resource_path_prefixes(deployment)
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
    diagnostics_prefix: str,
) -> None:
    secured_routes = []
    for route in getattr(router, "_routes", []):
        route_path = getattr(route, "path_template", None) or getattr(route, "path", "")
        if not _requires_admin_security_metadata(
            str(route_path),
            deployment,
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


