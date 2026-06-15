"""Public API front-door contract for Tigrbl Auth."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PublicApiContract:
    """Machine-readable boundary for the public OAuth/OIDC API package."""

    product_surface: str
    intended_uix: str
    baseline_capabilities: tuple[str, ...]
    production_capabilities: tuple[str, ...]
    forbidden_route_prefixes: tuple[str, ...]
    forbidden_exact_routes: tuple[str, ...]
    consumed_packages: tuple[str, ...]


PUBLIC_API_CONTRACT = PublicApiContract(
    product_surface="public-api",
    intended_uix="@tigrbl-auth/public-uix",
    baseline_capabilities=(
        "login",
        "authorize",
        "token",
        "openid-configuration",
        "tenant-openid-configuration",
        "oauth-authorization-server-metadata",
        "jwks",
        "tenant-jwks",
    ),
    production_capabilities=(
        "login",
        "authorize",
        "token",
        "userinfo",
        "introspection",
        "register",
        "register-management",
        "revoke",
        "logout",
        "openid-configuration",
        "tenant-openid-configuration",
        "oauth-authorization-server-metadata",
        "oauth-protected-resource-metadata",
        "jwks",
        "tenant-jwks",
    ),
    forbidden_route_prefixes=(
        "/admin",
        "/tenant/",
        "/diagnostics",
    ),
    forbidden_exact_routes=(
        "/rpc",
        "/tenant",
    ),
    consumed_packages=(
        "tigrbl-auth",
        "tigrbl-identity-server",
        "tigrbl-identity-runtime",
        "tigrbl-auth-protocol-oauth",
        "tigrbl-auth-protocol-oidc",
        "tigrbl-identity-jose",
    ),
)

__all__ = ["PUBLIC_API_CONTRACT", "PublicApiContract"]
