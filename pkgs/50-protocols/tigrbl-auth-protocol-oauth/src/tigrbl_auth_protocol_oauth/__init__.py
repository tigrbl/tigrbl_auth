"""Versioned OAuth authorization-framework and extension protocol ownership."""

from __future__ import annotations

from tigrbl_identity_contracts.protocol_processing import (
    build_protocol_capability_report,
)

from .bindings import CAPABILITY_REQUIREMENTS
from .claims import (
    OAUTH_DPOP_PROOF_CLAIMS,
    OAUTH_EXTENSION_CLAIMS,
    OAUTH_TOKEN_EXCHANGE_CLAIMS,
    compose_dpop_proof_claim_set,
    compose_oauth_claim_set,
    compose_token_exchange_claim_set,
)
from .compatibility import COMPATIBILITY_PATHS, OAuthCompatibility, compatibility
from .errors import OAuthBindingError, OAuthProtocolError, UnsupportedOAuthRevisionError
from .features import FEATURES_BY_VERSION, supports
from .migrations import REMOVED_GRANTS, migrate_client
from .protocol import (
    DPoPProof,
    DeviceAuthorization,
    InMemoryOAuthRepository,
    OAuthClient,
    OAuthError,
    OAuthGrantStatus,
    OAuthProtocolService,
    OAuthRepositoryPort,
    TokenExchangeResult,
    sha256_thumbprint,
)
from .schemas import (
    AuthorizationCodeGrantForm,
    DeviceAuthorizationIn,
    DeviceAuthorizationOut,
    DynamicClientRegistrationIn,
    DynamicClientRegistrationManagementIn,
    DynamicClientRegistrationOut,
    IntrospectOut,
    PasswordGrantForm,
    PushedAuthorizationRequestIn,
    PushedAuthorizationResponse,
    RefreshIn,
    RevocationIn,
    RevocationOut,
    TokenPair,
)
from .versions import (
    CURRENT_VERSION,
    EXTENSION_SPECIFICATIONS,
    VERSION_HISTORY,
    OAuthExtensionSpecification,
    OAuthVersion,
    select_version,
)


def capability_report() -> dict[str, object]:
    return build_protocol_capability_report(
        protocol="oauth",
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
    "EXTENSION_SPECIFICATIONS",
    "FEATURES_BY_VERSION",
    "OAUTH_DPOP_PROOF_CLAIMS",
    "OAUTH_EXTENSION_CLAIMS",
    "OAUTH_TOKEN_EXCHANGE_CLAIMS",
    "REMOVED_GRANTS",
    "VERSION_HISTORY",
    "AuthorizationCodeGrantForm",
    "DPoPProof",
    "DeviceAuthorization",
    "DeviceAuthorizationIn",
    "DeviceAuthorizationOut",
    "DynamicClientRegistrationIn",
    "DynamicClientRegistrationManagementIn",
    "DynamicClientRegistrationOut",
    "InMemoryOAuthRepository",
    "IntrospectOut",
    "OAuthBindingError",
    "OAuthClient",
    "OAuthCompatibility",
    "OAuthError",
    "OAuthExtensionSpecification",
    "OAuthGrantStatus",
    "OAuthProtocolError",
    "OAuthProtocolService",
    "OAuthRepositoryPort",
    "OAuthVersion",
    "PasswordGrantForm",
    "PushedAuthorizationRequestIn",
    "PushedAuthorizationResponse",
    "RefreshIn",
    "RevocationIn",
    "RevocationOut",
    "TokenExchangeResult",
    "TokenPair",
    "UnsupportedOAuthRevisionError",
    "capability_report",
    "compatibility",
    "compose_dpop_proof_claim_set",
    "compose_oauth_claim_set",
    "compose_token_exchange_claim_set",
    "migrate_client",
    "select_version",
    "sha256_thumbprint",
    "supports",
]
