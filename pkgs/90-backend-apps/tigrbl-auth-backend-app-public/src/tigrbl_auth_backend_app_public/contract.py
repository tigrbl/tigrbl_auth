"""Public backend-app contract for Tigrbl Auth."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PublicBackendAppContract:
    """Machine-readable boundary for the public OAuth/OIDC backend app."""

    product_surface: str
    intended_uix: str
    baseline_capabilities: tuple[str, ...]
    production_capabilities: tuple[str, ...]
    forbidden_route_prefixes: tuple[str, ...]
    forbidden_exact_routes: tuple[str, ...]
    consumed_packages: tuple[str, ...]
    mounted_router_packages: tuple[str, ...]
    app_local_route_groups: tuple[str, ...]


PUBLIC_BACKEND_APP_CONTRACT = PublicBackendAppContract(
    product_surface="public-app",
    intended_uix="@tigrbl-auth/public-uix",
    baseline_capabilities=(
        "login",
        "authorize",
        "token",
        "rest-only",
        "openid-configuration",
        "tenant-openid-configuration",
        "oauth-authorization-server-metadata",
        "jwks",
        "tenant-jwks",
        "standards-manifest",
        "oid4vci-credential",
        "oid4vp-verification",
        "authzen-evaluation",
        "gnap-transaction",
        "set-receiver",
        "attestation-appraisal",
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
        "standards-manifest",
        "oid4vci-credential",
        "oid4vp-verification",
        "authzen-evaluation",
        "gnap-transaction",
        "set-receiver",
        "attestation-appraisal",
    ),
    forbidden_route_prefixes=(
        "/admin",
        "/cryptokey",
        "/cryptokeyversion",
        "/principalkeybinding",
        "/keyenvelope",
        "/keyattestationevidence",
        "/tenant/",
        "/diagnostics",
    ),
    forbidden_exact_routes=("/tenant",),
    consumed_packages=(
        "tigrbl-auth",
        "tigrbl-identity-server",
        "tigrbl-identity-runtime",
        "tigrbl-auth-protocol-oauth",
        "tigrbl-auth-protocol-oidc",
        "tigrbl-identity-jose",
        "tigrbl-auth-protocol-oid4vci",
        "tigrbl-auth-protocol-oid4vp",
        "tigrbl-auth-profile-haip",
    ),
    mounted_router_packages=(
        "tigrbl-auth-router-oauth-authorization",
        "tigrbl-auth-router-oauth-authorization-server-metadata",
        "tigrbl-auth-router-oauth-device-authorization",
        "tigrbl-auth-router-oauth-introspection",
        "tigrbl-auth-router-oauth-par",
        "tigrbl-auth-router-oauth-protected-resource-metadata",
        "tigrbl-auth-router-oauth-registration",
        "tigrbl-auth-router-oauth-revocation",
        "tigrbl-auth-router-oauth-token",
        "tigrbl-auth-router-oauth-token-exchange",
        "tigrbl-auth-router-oidc-discovery",
        "tigrbl-auth-router-oidc-logout",
        "tigrbl-auth-router-oidc-userinfo",
        "tigrbl-auth-router-session-login",
        "tigrbl-auth-router-webauthn",
    ),
    app_local_route_groups=(),
)

__all__ = ["PUBLIC_BACKEND_APP_CONTRACT", "PublicBackendAppContract"]
