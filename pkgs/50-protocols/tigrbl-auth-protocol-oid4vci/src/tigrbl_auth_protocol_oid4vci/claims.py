"""Standalone claim classes used by OID4VCI proof JWTs."""

from tigrbl_claim_audience_concrete import AudienceClaim
from tigrbl_claim_issued_at_concrete import IssuedAtClaim
from tigrbl_claim_nonce_concrete import NonceClaim
from tigrbl_identity_contracts.claims import ClaimSet

from .versions import CURRENT_VERSION

OID4VCI_PROOF_CLAIM_CLASSES = (AudienceClaim, IssuedAtClaim, NonceClaim)


def compose_oid4vci_proof_claim_set(*claims: object) -> ClaimSet:
    return ClaimSet(tuple(claims), "oid4vci-proof", CURRENT_VERSION.identifier)


__all__ = ["OID4VCI_PROOF_CLAIM_CLASSES", "compose_oid4vci_proof_claim_set"]
