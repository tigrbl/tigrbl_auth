"""Service-admin backend-app contract for Tigrbl Auth."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ServiceAdminBackendAppContract:
    """Machine-readable boundary for the service/workload backend app."""

    product_surface: str
    intended_uix: str
    public_capabilities: tuple[str, ...]
    admin_resources: tuple[str, ...]
    admin_rest_groups: tuple[str, ...]
    forbidden_route_prefixes: tuple[str, ...]
    forbidden_exact_routes: tuple[str, ...]
    consumed_packages: tuple[str, ...]
    mounted_router_packages: tuple[str, ...]
    app_local_route_groups: tuple[str, ...]


SERVICE_ADMIN_BACKEND_APP_CONTRACT = ServiceAdminBackendAppContract(
    product_surface="service-admin-app",
    intended_uix="@tigrbl-auth/service-admin-uix",
    public_capabilities=(
        "introspection",
        "openid-configuration",
        "tenant-openid-configuration",
        "realm-openid-configuration",
        "oauth-protected-resource-metadata",
        "jwks",
        "tenant-jwks",
        "realm-jwks",
    ),
    admin_resources=(
        "CredentialApiKey",
        "ServiceIdentity",
        "CredentialServiceKey",
        "TokenRecord",
        "AuditEvent",
    ),
    admin_rest_groups=(),
    forbidden_route_prefixes=(
        "/tenant",
        "/user",
        "/authsession",
        "/consent",
        "/client",
        "/clientregistration",
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
    ),
    consumed_packages=(
        "tigrbl-auth",
        "tigrbl-identity-server",
        "tigrbl-identity-runtime",
        "tigrbl-identity-admin",
        "tigrbl-identity-principals",
        "tigrbl-authz-policy",
        "tigrbl-authz-resource-server",
        "tigrbl-auth-protocol-oauth",
        "tigrbl-auth-protocol-oidc",
    ),
    mounted_router_packages=(
        "tigrbl-auth-router-admin-gate",
        "tigrbl-auth-router-oauth-introspection",
        "tigrbl-auth-router-oauth-protected-resource-metadata",
        "tigrbl-auth-router-oidc-discovery",
    ),
    app_local_route_groups=(),
)

__all__ = ["SERVICE_ADMIN_BACKEND_APP_CONTRACT", "ServiceAdminBackendAppContract"]
