"""Developer backend-app contract for TBA."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DeveloperBackendAppContract:
    """Machine-readable boundary for the developer self-service backend app."""

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


DEVELOPER_BACKEND_APP_CONTRACT = DeveloperBackendAppContract(
    product_surface="developer-app",
    intended_uix="@tba/ui-developer",
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
        "/serviceidentity",
        "/credentialservicekey",
        "/credentialapikey",
        "/cryptokey",
        "/cryptokeyversion",
        "/principalkeybinding",
        "/keyenvelope",
        "/keyattestationevidence",
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
        "tba-auth",
        "tba-server-identity",
        "tba-runtime-identity",
        "tba-runtime-identity-administration",
        "tba-concrete-identity-principals",
        "tba-protocol-oauth",
        "tba-protocol-oidc",
    ),
    mounted_router_packages=(
        "tba-router-administration-gate",
        "tba-router-oauth-authorization-server-metadata",
        "tba-router-oauth-registration",
        "tba-router-oidc-discovery",
    ),
    app_local_route_groups=(),
)

__all__ = ["DEVELOPER_BACKEND_APP_CONTRACT", "DeveloperBackendAppContract"]
