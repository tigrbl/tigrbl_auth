"""Platform-admin API front-door contract for Tigrbl Auth."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PlatformAdminApiContract:
    """Machine-readable boundary for the platform control-plane API package."""

    product_surface: str
    intended_uix: str
    admin_resources: tuple[str, ...]
    admin_rest_groups: tuple[str, ...]
    forbidden_route_prefixes: tuple[str, ...]
    forbidden_exact_routes: tuple[str, ...]
    consumed_packages: tuple[str, ...]


PLATFORM_ADMIN_API_CONTRACT = PlatformAdminApiContract(
    product_surface="platform-admin-api",
    intended_uix="@tigrbl-auth/platform-admin-uix",
    admin_resources=(
        "Realm",
        "Tenant",
        "User",
        "AuditEvent",
        "KeyRotationEvent",
    ),
    admin_rest_groups=("admin_auth", "admin_realms", "admin_identities"),
    forbidden_route_prefixes=(
        "/client",
        "/clientregistration",
        "/consent",
        "/service",
        "/servicekey",
        "/apikey",
        "/tokenrecord",
        "/revokedtoken",
        "/authsession",
        "/tenant",
        "/user",
    ),
    forbidden_exact_routes=(
        "/login",
        "/authorize",
        "/token",
        "/register",
        "/logout",
        "/revoke",
        "/userinfo",
        "/introspect",
        "/rpc",
        "/openrpc.json",
        "/.well-known/jwks.json",
        "/.well-known/openid-configuration",
    ),
    consumed_packages=(
        "tigrbl-auth",
        "tigrbl-identity-server",
        "tigrbl-identity-runtime",
        "tigrbl-identity-admin",
        "tigrbl-identity-principals",
        "tigrbl-authz-policy",
    ),
)

__all__ = ["PLATFORM_ADMIN_API_CONTRACT", "PlatformAdminApiContract"]
