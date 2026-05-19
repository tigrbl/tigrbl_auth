"""Compatibility facade for canonical RFC 9449 DPoP helpers."""

from tigrbl_auth.standards.oauth2.dpop import (
    RFC9449_SPEC_URL,
    DPoPNonceRecord,
    DPoPReplayStore,
    access_token_hash,
    decode_proof,
    issue_nonce,
    jwk_from_public_key,
    jwk_thumbprint,
    make_proof,
    replay_store_snapshot,
    verify_proof,
)

makeProof = make_proof
create_proof = make_proof

__all__ = [
    "RFC9449_SPEC_URL",
    "DPoPNonceRecord",
    "DPoPReplayStore",
    "access_token_hash",
    "decode_proof",
    "issue_nonce",
    "jwk_from_public_key",
    "jwk_thumbprint",
    "make_proof",
    "makeProof",
    "create_proof",
    "replay_store_snapshot",
    "verify_proof",
]
