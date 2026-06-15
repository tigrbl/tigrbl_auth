"""Resource-validation API front-door contract for Tigrbl Auth."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ResourceValidationApiContract:
    """Machine-readable boundary for resource-server validation metadata."""

    product_surface: str
    intended_consumers: tuple[str, ...]
    production_capabilities: tuple[str, ...]
    forbidden_route_prefixes: tuple[str, ...]
    forbidden_exact_routes: tuple[str, ...]
    consumed_packages: tuple[str, ...]


RESOURCE_VALIDATION_API_CONTRACT = ResourceValidationApiContract(
    product_surface="resource-validation-api",
    intended_consumers=(
        "tigrbl-authz-resource-server",
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
        "tigrbl-auth",
        "tigrbl-identity-server",
        "tigrbl-identity-runtime",
        "tigrbl-identity-jose",
        "tigrbl-authz-resource-server",
    ),
)

__all__ = [
    "RESOURCE_VALIDATION_API_CONTRACT",
    "ResourceValidationApiContract",
]
