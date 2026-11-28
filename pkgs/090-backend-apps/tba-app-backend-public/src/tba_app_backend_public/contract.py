"""Public backend-app contract for TBA."""

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
    intended_uix="@tba/ui-public",
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
        "tba-auth",
        "tba-server-identity",
        "tba-runtime-identity",
        "tba-protocol-oauth",
        "tba-protocol-oidc",
        "tba-provider-identity-jose",
        "tba-protocol-oid4vci",
        "tba-protocol-oid4vp",
        "tba-profile-haip",
    ),
    mounted_router_packages=(
        "tba-router-oauth-authorization",
        "tba-router-oauth-authorization-server-metadata",
        "tba-router-oauth-device-authorization",
        "tba-router-oauth-introspection",
        "tba-router-oauth-pushed-authorization-request",
        "tba-router-oauth-protected-resource-metadata",
        "tba-router-oauth-registration",
        "tba-router-oauth-revocation",
        "tba-router-oauth-token",
        "tba-router-oauth-token-exchange",
        "tba-router-oidc-discovery",
        "tba-router-oidc-logout",
        "tba-router-oidc-userinfo",
        "tba-router-session-login",
        "tba-router-webauthn",
    ),
    app_local_route_groups=(),
)

__all__ = ["PUBLIC_BACKEND_APP_CONTRACT", "PublicBackendAppContract"]
