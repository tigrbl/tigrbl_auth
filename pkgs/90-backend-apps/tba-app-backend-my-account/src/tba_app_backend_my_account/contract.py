"""My Account backend-app contract for TBA."""

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
    intended_uix="@tba/ui-my-account",
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
        "tba-auth",
        "tba-server-identity",
        "tba-runtime-identity",
        "tba-concrete-identity-principals",
        "tba-credentials",
        "tba-runtime-authorization-policy",
        "tba-protocol-oidc",
        "tba-storage-core",
    ),
    mounted_router_packages=("tba-router-oidc-discovery",),
    app_local_route_groups=(
        "profiles",
        "sessions",
        "consents",
        "credentials",
    ),
)

__all__ = ["MY_ACCOUNT_BACKEND_APP_CONTRACT", "MyAccountBackendAppContract"]
