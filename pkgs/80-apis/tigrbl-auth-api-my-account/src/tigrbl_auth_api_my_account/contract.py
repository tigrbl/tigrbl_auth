"""My Account API front-door contract for Tigrbl Auth."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MyAccountApiContract:
    """Machine-readable boundary for the end-user account API package."""

    product_surface: str
    intended_uix: str
    baseline_capabilities: tuple[str, ...]
    forbidden_route_prefixes: tuple[str, ...]
    forbidden_exact_routes: tuple[str, ...]
    consumed_packages: tuple[str, ...]


MY_ACCOUNT_API_CONTRACT = MyAccountApiContract(
    product_surface="my-account-api",
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
)

__all__ = ["MY_ACCOUNT_API_CONTRACT", "MyAccountApiContract"]
