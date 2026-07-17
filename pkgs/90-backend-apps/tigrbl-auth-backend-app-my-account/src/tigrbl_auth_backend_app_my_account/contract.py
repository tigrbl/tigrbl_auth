"""My Account backend-app contract for Tigrbl Auth."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MyAccountBackendAppContract:
    """Machine-readable boundary for the end-user account backend app."""

    product_surface: str
    intended_uix: str
    baseline_capabilities: tuple[str, ...]
    forbidden_route_prefixes: tuple[str, ...]
    forbidden_exact_routes: tuple[str, ...]
    consumed_packages: tuple[str, ...]
    mounted_router_packages: tuple[str, ...]
    app_local_route_groups: tuple[str, ...]


MY_ACCOUNT_BACKEND_APP_CONTRACT = MyAccountBackendAppContract(
    product_surface="my-account-app",
    intended_uix="@tigrbl-auth/my-account-uix",
    baseline_capabilities=(
        "account-profile",
        "account-sessions",
        "account-consents",
        "account-credentials",
        "rest-only",
        "openid-configuration",
        "tenant-openid-configuration",
        "jwks",
        "tenant-jwks",
    ),
    forbidden_route_prefixes=(
        "/admin",
        "/tenant",
        "/client",
        "/serviceidentity",
        "/user",
        "/credentialapikey",
        "/credentialservicekey",
        "/cryptokey",
        "/cryptokeyversion",
        "/principalkeybinding",
        "/keyenvelope",
        "/keyattestationevidence",
        "/tokenrecord",
        "/authsession",
        "/auditevent",
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
    ),
    consumed_packages=(
        "tigrbl-auth",
        "tigrbl-identity-server",
        "tigrbl-identity-runtime",
        "tigrbl-identity-principals",
        "tigrbl-authn-credentials",
        "tigrbl-authz-policy",
        "tigrbl-auth-protocol-oidc",
        "tigrbl-identity-storage",
    ),
    mounted_router_packages=("tigrbl-auth-router-oidc-discovery",),
    app_local_route_groups=(
        "profiles",
        "sessions",
        "consents",
        "credentials",
    ),
)

__all__ = ["MY_ACCOUNT_BACKEND_APP_CONTRACT", "MyAccountBackendAppContract"]
