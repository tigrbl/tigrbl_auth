"""Service-admin API front-door contract for Tigrbl Auth."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ServiceAdminApiContract:
    """Machine-readable boundary for the service/workload API package."""

    product_surface: str
    intended_uix: str
    public_capabilities: tuple[str, ...]
    admin_resources: tuple[str, ...]
    admin_rest_groups: tuple[str, ...]
    forbidden_route_prefixes: tuple[str, ...]
    forbidden_exact_routes: tuple[str, ...]
    consumed_packages: tuple[str, ...]


SERVICE_ADMIN_API_CONTRACT = ServiceAdminApiContract(
    product_surface="service-admin-api",
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
)

__all__ = ["SERVICE_ADMIN_API_CONTRACT", "ServiceAdminApiContract"]
