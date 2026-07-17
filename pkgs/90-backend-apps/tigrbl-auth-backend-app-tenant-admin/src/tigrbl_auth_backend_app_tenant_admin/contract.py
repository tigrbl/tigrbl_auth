"""Tenant-admin backend-app contract for Tigrbl Auth."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TenantAdminBackendAppContract:
    """Machine-readable boundary for the tenant control-plane backend app."""

    product_surface: str
    intended_uix: str
    admin_resources: tuple[str, ...]
    admin_rest_groups: tuple[str, ...]
    forbidden_route_prefixes: tuple[str, ...]
    forbidden_exact_routes: tuple[str, ...]
    consumed_packages: tuple[str, ...]
    mounted_router_packages: tuple[str, ...]
    app_local_route_groups: tuple[str, ...]


TENANT_ADMIN_BACKEND_APP_CONTRACT = TenantAdminBackendAppContract(
    product_surface="tenant-admin-app",
    intended_uix="@tigrbl-auth/tenant-admin-uix",
    admin_resources=(
        "User",
        "Client",
        "ClientRegistration",
        "Consent",
        "AuditEvent",
        "CryptoKey",
        "CryptoKeyVersion",
        "PrincipalKeyBinding",
        "KeyEnvelope",
        "KeyAttestationEvidence",
        "KeyRotationEvent",
    ),
    admin_rest_groups=("admin_auth", "admin_identities"),
    forbidden_route_prefixes=(
        "/tenant",
        "/serviceidentity",
        "/credentialservicekey",
        "/credentialapikey",
        "/tokenrecord",
        "/revokedtoken",
        "/authsession",
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
    mounted_router_packages=("tigrbl-auth-router-admin-gate",),
    app_local_route_groups=(),
)

__all__ = ["TENANT_ADMIN_BACKEND_APP_CONTRACT", "TenantAdminBackendAppContract"]
