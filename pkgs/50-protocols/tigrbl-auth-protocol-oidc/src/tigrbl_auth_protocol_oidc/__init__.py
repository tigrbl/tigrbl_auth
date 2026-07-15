"""Versioned OpenID Connect provider protocol ownership."""

from __future__ import annotations

from tigrbl_identity_contracts.protocol_processing import (
    build_protocol_capability_report,
)

from .bindings import CAPABILITY_REQUIREMENTS
from .claims import (
    OIDC_EXTENSION_CLAIMS,
    OIDC_ID_TOKEN_PROFILE_CLAIMS,
    OIDC_USERINFO_CLAIMS,
    compose_oidc_claim_set,
    compose_oidc_id_token_claim_set,
    compose_oidc_userinfo_claim_set,
)
from .compatibility import COMPATIBILITY_PATHS, OidcCompatibility, compatibility
from .errors import OidcBindingError, OidcProtocolError, UnsupportedOidcRevisionError
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
from .schemas import LogoutIn, LogoutOut
from .versions import CURRENT_VERSION, VERSION_HISTORY, OidcVersion, select_version


def capability_report() -> dict[str, object]:
    return build_protocol_capability_report(
        protocol="oidc",
        revision=CURRENT_VERSION.identifier,
        features=tuple(FEATURES_BY_VERSION[CURRENT_VERSION.identifier]),
        evidence_links=("tests/unit/test_versioned_oauth_oidc_protocols.py",),
        extra_requirements=CAPABILITY_REQUIREMENTS,
        include_default_artifact_requirements=False,
    )


__all__ = [
    "CAPABILITY_REQUIREMENTS",
    "COMPATIBILITY_PATHS",
    "CURRENT_VERSION",
    "FEATURES_BY_VERSION",
    "OIDC_EXTENSION_CLAIMS",
    "OIDC_ID_TOKEN_PROFILE_CLAIMS",
    "OIDC_USERINFO_CLAIMS",
    "VERSION_HISTORY",
    "HostedLoginPage",
    "HostedLoginRequest",
    "LoginThemeAssetPolicy",
    "LogoutIn",
    "LogoutOut",
    "LogoutPlan",
    "LogoutRequest",
    "OidcBindingError",
    "OidcCompatibility",
    "OidcProtocolError",
    "OidcProviderError",
    "OidcProviderRuntime",
    "OidcSession",
    "OidcSessionStatus",
    "OidcVersion",
    "TenantBranding",
    "TenantBrandingRegistry",
    "UnsupportedOidcRevisionError",
    "capability_report",
    "compatibility",
    "compose_oidc_claim_set",
    "compose_oidc_id_token_claim_set",
    "compose_oidc_userinfo_claim_set",
    "migrate_client_metadata",
    "new_login_request",
    "render_login_template",
    "select_version",
    "supports",
]
