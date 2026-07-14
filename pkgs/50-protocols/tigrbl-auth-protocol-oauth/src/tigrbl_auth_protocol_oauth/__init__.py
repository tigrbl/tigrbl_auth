"""OAuth protocol surfaces for the Tigrbl identity package suite."""

from __future__ import annotations

from .claim_sets import (
    OAUTH_DPOP_PROOF_CLAIMS,
    OAUTH_EXTENSION_CLAIMS,
    OAUTH_TOKEN_EXCHANGE_CLAIMS,
    compose_dpop_proof_claim_set,
    compose_oauth_claim_set,
    compose_token_exchange_claim_set,
)
from .features import FEATURES_BY_VERSION, supports
from .migrations import REMOVED_GRANTS, migrate_client
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
from .versions import CURRENT_VERSION, VERSION_HISTORY, OAuthVersion, select_version
from .capability_requirements import CAPABILITY_REQUIREMENTS

__all__ = [
    "DPoPProof",
    "AuthorizationCodeGrantForm",
    "CURRENT_VERSION",
    "CAPABILITY_REQUIREMENTS",
    "DeviceAuthorization",
    "DeviceAuthorizationIn",
    "DeviceAuthorizationOut",
    "DynamicClientRegistrationIn",
    "DynamicClientRegistrationManagementIn",
    "DynamicClientRegistrationOut",
    "InMemoryOAuthRepository",
    "OAuthClient",
    "OAuthError",
    "OAuthGrantStatus",
    "OAuthProtocolService",
    "OAuthRepositoryPort",
    "IntrospectOut",
    "OAUTH_EXTENSION_CLAIMS",
    "OAUTH_DPOP_PROOF_CLAIMS",
    "OAUTH_TOKEN_EXCHANGE_CLAIMS",
    "FEATURES_BY_VERSION",
    "REMOVED_GRANTS",
    "PasswordGrantForm",
    "PushedAuthorizationRequestIn",
    "PushedAuthorizationResponse",
    "RefreshIn",
    "RevocationIn",
    "RevocationOut",
    "TokenPair",
    "TokenExchangeResult",
    "compose_oauth_claim_set",
    "compose_dpop_proof_claim_set",
    "compose_token_exchange_claim_set",
    "migrate_client",
    "select_version",
    "sha256_thumbprint",
    "supports",
    "VERSION_HISTORY",
    "OAuthVersion",
]


from tigrbl_identity_contracts.protocol_processing import build_protocol_capability_report as _build_protocol_capability_report

def capability_report() -> dict[str, object]:
    return _build_protocol_capability_report(
        protocol='oauth',
        revision=CURRENT_VERSION.identifier,
        features=tuple(FEATURES_BY_VERSION[CURRENT_VERSION.identifier]),
        evidence_links=('tests/unit/test_versioned_oauth_oidc_protocols.py',),
        extra_requirements=tuple(globals().get('CAPABILITY_REQUIREMENTS', ())),
    )
