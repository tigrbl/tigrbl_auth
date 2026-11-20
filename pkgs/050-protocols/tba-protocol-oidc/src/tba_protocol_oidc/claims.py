"""Canonical OIDC Core and extension claim-set ownership."""

from .claim_sets import (
    OIDC_EXTENSION_CLAIMS,
    OIDC_ID_TOKEN_PROFILE_CLAIMS,
    OIDC_USERINFO_CLAIMS,
    compose_oidc_claim_set,
    compose_oidc_id_token_claim_set,
    compose_oidc_userinfo_claim_set,
)

__all__ = [
    "OIDC_EXTENSION_CLAIMS",
    "OIDC_ID_TOKEN_PROFILE_CLAIMS",
    "OIDC_USERINFO_CLAIMS",
    "compose_oidc_claim_set",
    "compose_oidc_id_token_claim_set",
    "compose_oidc_userinfo_claim_set",
]
