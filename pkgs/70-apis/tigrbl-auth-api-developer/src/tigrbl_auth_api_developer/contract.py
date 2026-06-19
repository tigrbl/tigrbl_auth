"""Developer API front-door contract for Tigrbl Auth."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DeveloperApiContract:
    """Machine-readable boundary for the developer self-service API package."""

    product_surface: str
    intended_uix: str
    public_capabilities: tuple[str, ...]
    admin_resources: tuple[str, ...]
    admin_rest_groups: tuple[str, ...]
    forbidden_route_prefixes: tuple[str, ...]
    forbidden_exact_routes: tuple[str, ...]
    consumed_packages: tuple[str, ...]


DEVELOPER_API_CONTRACT = DeveloperApiContract(
    product_surface="developer-api",
    intended_uix="@tigrbl-auth/developer-uix",
    public_capabilities=(
        "register",
        "register-management",
        "openid-configuration",
        "tenant-openid-configuration",
        "realm-openid-configuration",
        "oauth-authorization-server-metadata",
        "jwks",
        "tenant-jwks",
        "realm-jwks",
    ),
    admin_resources=("Client", "ClientRegistration", "AuditEvent"),
    admin_rest_groups=(),
    forbidden_route_prefixes=(
        "/tenant",
        "/user",
        "/authsession",
        "/consent",
        "/service",
        "/servicekey",
        "/apikey",
        "/tokenrecord",
        "/revokedtoken",
    ),
    forbidden_exact_routes=(
        "/login",
        "/authorize",
        "/token",
        "/logout",
        "/revoke",
        "/userinfo",
        "/introspect",
    ),
    consumed_packages=(
        "tigrbl-auth",
        "tigrbl-identity-server",
        "tigrbl-identity-runtime",
        "tigrbl-identity-admin",
        "tigrbl-identity-principals",
        "tigrbl-auth-protocol-oauth",
        "tigrbl-auth-protocol-oidc",
    ),
)

__all__ = ["DEVELOPER_API_CONTRACT", "DeveloperApiContract"]
