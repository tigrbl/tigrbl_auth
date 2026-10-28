"""Resource-validation backend-app contract for TBA."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ResourceValidationBackendAppContract:
    """Machine-readable boundary for resource-server validation metadata."""

    product_surface: str
    intended_consumers: tuple[str, ...]
    production_capabilities: tuple[str, ...]
    forbidden_route_prefixes: tuple[str, ...]
    forbidden_exact_routes: tuple[str, ...]
    consumed_packages: tuple[str, ...]
    mounted_router_packages: tuple[str, ...]
    app_local_route_groups: tuple[str, ...]


RESOURCE_VALIDATION_BACKEND_APP_CONTRACT = ResourceValidationBackendAppContract(
    product_surface="resource-validation-app",
    intended_consumers=(
        "tba-protocol-authorization-resource-server",
        "protected API gateways",
        "resource-server validation middleware",
    ),
    production_capabilities=(
        "introspection",
        "openid-configuration",
        "tenant-openid-configuration",
        "oauth-protected-resource-metadata",
        "jwks",
        "tenant-jwks",
    ),
    forbidden_route_prefixes=(
        "/admin",
        "/tenant/",
        "/register/",
        "/diagnostics",
        "/cryptokey",
        "/cryptokeyversion",
        "/principalkeybinding",
        "/keyenvelope",
        "/keyattestationevidence",
    ),
    forbidden_exact_routes=(
        "/login",
        "/authorize",
        "/token",
        "/register",
        "/logout",
        "/revoke",
        "/userinfo",
        "/device_authorization",
        "/par",
        "/token/exchange",
        "/rpc",
        "/tenant",
    ),
    consumed_packages=(
        "tba-auth",
        "tba-server-identity",
        "tba-runtime-identity",
        "tba-provider-identity-jose",
        "tba-protocol-authorization-resource-server",
    ),
    mounted_router_packages=(
        "tba-router-oauth-introspection",
        "tba-router-oauth-protected-resource-metadata",
        "tba-router-oidc-discovery",
        "tba-router-resource-validation-metadata",
    ),
    app_local_route_groups=(),
)

__all__ = [
    "RESOURCE_VALIDATION_BACKEND_APP_CONTRACT",
    "ResourceValidationBackendAppContract",
]
