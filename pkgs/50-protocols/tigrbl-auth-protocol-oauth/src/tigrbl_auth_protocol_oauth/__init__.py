"""OAuth protocol surfaces for the Tigrbl identity package suite."""

from __future__ import annotations

from .claim_sets import OAUTH_EXTENSION_CLAIMS, compose_oauth_claim_set
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

__all__ = [
    "DPoPProof",
    "DeviceAuthorization",
    "InMemoryOAuthRepository",
    "OAuthClient",
    "OAuthError",
    "OAuthGrantStatus",
    "OAuthProtocolService",
    "OAuthRepositoryPort",
    "OAUTH_EXTENSION_CLAIMS",
    "TokenExchangeResult",
    "compose_oauth_claim_set",
    "sha256_thumbprint",
]
