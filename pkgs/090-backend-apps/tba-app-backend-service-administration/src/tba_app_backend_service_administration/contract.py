"""Service-admin backend-app contract for TBA."""

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
    intended_uix="@tba/ui-service-administration",
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
        "tba-auth",
        "tba-server-identity",
        "tba-runtime-identity",
        "tba-runtime-identity-administration",
        "tba-concrete-identity-principals",
        "tba-runtime-authorization-policy",
        "tba-protocol-oauth-protected-resource",
        "tba-protocol-oauth",
        "tba-protocol-oidc",
    ),
    mounted_router_packages=(
        "tba-router-administration-gate",
        "tba-router-oauth-introspection",
        "tba-router-oauth-protected-resource-metadata",
        "tba-router-oidc-discovery",
    ),
    app_local_route_groups=(),
)

__all__ = ["SERVICE_ADMIN_BACKEND_APP_CONTRACT", "ServiceAdminBackendAppContract"]
