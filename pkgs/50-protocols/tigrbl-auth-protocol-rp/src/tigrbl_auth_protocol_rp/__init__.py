"""Versioned OIDC relying-party and OAuth client composite profile."""

from __future__ import annotations

from tigrbl_identity_contracts.protocol_processing import (
    build_protocol_capability_report,
)

from .bindings import CAPABILITY_REQUIREMENTS
from .claims import RP_ID_TOKEN_CLAIMS, compose_rp_id_token_claim_set
from .client import (
    BrowserMemorySession,
    BrowserStoragePolicy,
    CallbackResult,
    DiscoveryClient,
    JwksCache,
    LoginRequest,
    PkceVerifier,
    RPConfiguration,
    RPSession,
    RelyingParty,
    UserInfoClient,
    assert_browser_no_client_secret,
    example_app_manifest,
    framework_callback_adapter,
    framework_login_adapter,
    make_pkce_verifier,
    pkce_s256_challenge,
    shared_vector_manifest,
    validate_browser_storage_policy,
    validate_id_token_claims,
)
from .compatibility import COMPATIBILITY_PATHS, RpCompatibility, compatibility
from .errors import RPError, UnsupportedRpProfileError
from .features import FEATURES_BY_VERSION, supports
from .migrations import migrate_configuration
from .versions import (
    CURRENT_VERSION,
    VERSION_HISTORY,
    RpProfileVersion,
    select_version,
)


def capability_report() -> dict[str, object]:
    return build_protocol_capability_report(
        protocol="rp",
        revision=CURRENT_VERSION.identifier,
        features=tuple(FEATURES_BY_VERSION[CURRENT_VERSION.identifier]),
        evidence_links=("tests/unit/test_rp_consumer_boundary.py",),
        extra_requirements=CAPABILITY_REQUIREMENTS,
        include_default_artifact_requirements=False,
    )


__all__ = [
    "CAPABILITY_REQUIREMENTS",
    "COMPATIBILITY_PATHS",
    "CURRENT_VERSION",
    "FEATURES_BY_VERSION",
    "RP_ID_TOKEN_CLAIMS",
    "VERSION_HISTORY",
    "BrowserMemorySession",
    "BrowserStoragePolicy",
    "CallbackResult",
    "DiscoveryClient",
    "JwksCache",
    "LoginRequest",
    "PkceVerifier",
    "RPConfiguration",
    "RPError",
    "RPSession",
    "RelyingParty",
    "RpCompatibility",
    "RpProfileVersion",
    "UnsupportedRpProfileError",
    "UserInfoClient",
    "assert_browser_no_client_secret",
    "capability_report",
    "compatibility",
    "compose_rp_id_token_claim_set",
    "example_app_manifest",
    "framework_callback_adapter",
    "framework_login_adapter",
    "make_pkce_verifier",
    "migrate_configuration",
    "pkce_s256_challenge",
    "select_version",
    "shared_vector_manifest",
    "supports",
    "validate_browser_storage_policy",
    "validate_id_token_claims",
]
