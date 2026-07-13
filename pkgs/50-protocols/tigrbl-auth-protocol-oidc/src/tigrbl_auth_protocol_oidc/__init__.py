"""OpenID Connect provider surfaces for the Tigrbl identity package suite."""

from __future__ import annotations

from .claim_sets import (
    OIDC_EXTENSION_CLAIMS,
    OIDC_ID_TOKEN_PROFILE_CLAIMS,
    OIDC_USERINFO_CLAIMS,
    compose_oidc_claim_set,
    compose_oidc_id_token_claim_set,
    compose_oidc_userinfo_claim_set,
)
from .features import FEATURES_BY_VERSION, supports
from .migrations import migrate_client_metadata
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
from .versions import CURRENT_VERSION, VERSION_HISTORY, OidcVersion, select_version
from .capability_requirements import CAPABILITY_REQUIREMENTS

__all__ = [
    "OIDC_EXTENSION_CLAIMS",
    "OIDC_ID_TOKEN_PROFILE_CLAIMS",
    "OIDC_USERINFO_CLAIMS",
    "CURRENT_VERSION",
    "CAPABILITY_REQUIREMENTS",
    "FEATURES_BY_VERSION",
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
    "compose_oidc_id_token_claim_set",
    "compose_oidc_userinfo_claim_set",
    "migrate_client_metadata",
    "new_login_request",
    "render_login_template",
    "select_version",
    "supports",
    "VERSION_HISTORY",
    "OidcVersion",
]


from tigrbl_identity_contracts.protocol_processing import build_protocol_capability_report as _build_protocol_capability_report

def capability_report() -> dict[str, object]:
    return _build_protocol_capability_report(
        protocol='oidc',
        revision=CURRENT_VERSION.identifier,
        features=tuple(FEATURES_BY_VERSION[CURRENT_VERSION.identifier]),
        evidence_links=('tests/unit/test_versioned_oauth_oidc_protocols.py',),
        extra_requirements=tuple(globals().get('CAPABILITY_REQUIREMENTS', ())),
    )
