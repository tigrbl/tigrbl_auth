"""OAuth protocol surfaces for the Tigrbl identity package suite."""

from __future__ import annotations

from .claim_sets import OAUTH_EXTENSION_CLAIMS, compose_oauth_claim_set
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
from .versions import CURRENT_VERSION, VERSION_HISTORY, OAuthVersion, select_version

__all__ = [
    "DPoPProof",
    "CURRENT_VERSION",
    "DeviceAuthorization",
    "InMemoryOAuthRepository",
    "OAuthClient",
    "OAuthError",
    "OAuthGrantStatus",
    "OAuthProtocolService",
    "OAuthRepositoryPort",
    "OAUTH_EXTENSION_CLAIMS",
    "FEATURES_BY_VERSION",
    "REMOVED_GRANTS",
    "TokenExchangeResult",
    "compose_oauth_claim_set",
    "migrate_client",
    "select_version",
    "sha256_thumbprint",
    "supports",
    "VERSION_HISTORY",
    "OAuthVersion",
]
