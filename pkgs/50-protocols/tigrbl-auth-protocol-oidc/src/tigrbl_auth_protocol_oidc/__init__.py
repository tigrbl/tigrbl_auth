"""OpenID Connect provider surfaces for the Tigrbl identity package suite."""

from __future__ import annotations

from .claim_sets import OIDC_EXTENSION_CLAIMS, compose_oidc_claim_set
from .provider import (
    HostedLoginPage,
    HostedLoginRequest,
    LoginThemeAssetPolicy,
    LogoutPlan,
    LogoutRequest,
    OidcProviderError,
    OidcProviderRuntime,
    OidcSession,
    OidcSessionStatus,
    TenantBranding,
    TenantBrandingRegistry,
    new_login_request,
    render_login_template,
)

__all__ = [
    "OIDC_EXTENSION_CLAIMS",
    "HostedLoginPage",
    "HostedLoginRequest",
    "LoginThemeAssetPolicy",
    "LogoutPlan",
    "LogoutRequest",
    "OidcProviderError",
    "OidcProviderRuntime",
    "OidcSession",
    "OidcSessionStatus",
    "TenantBranding",
    "TenantBrandingRegistry",
    "compose_oidc_claim_set",
    "new_login_request",
    "render_login_template",
]
