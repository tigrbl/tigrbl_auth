"""Deprecated compatibility exports for :mod:`tigrbl_auth_protocol_oauth.claims`."""

from .claims import (
    OAUTH_DPOP_PROOF_CLAIMS,
    OAUTH_EXTENSION_CLAIMS,
    OAUTH_TOKEN_EXCHANGE_CLAIMS,
    compose_dpop_proof_claim_set,
    compose_oauth_claim_set,
    compose_token_exchange_claim_set,
)

__all__ = [
    "OAUTH_DPOP_PROOF_CLAIMS",
    "OAUTH_EXTENSION_CLAIMS",
    "OAUTH_TOKEN_EXCHANGE_CLAIMS",
    "compose_dpop_proof_claim_set",
    "compose_oauth_claim_set",
    "compose_token_exchange_claim_set",
]
