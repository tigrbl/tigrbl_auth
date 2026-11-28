"""Standalone claim classes used by OID4VCI proof JWTs."""

from tba_concrete_claim_audience import AudienceClaim
from tba_concrete_claim_issued_at import IssuedAtClaim
from tba_concrete_claim_nonce import NonceClaim
from tba_contracts_identity.claims import ClaimSet

from .versions import CURRENT_VERSION

OID4VCI_PROOF_CLAIM_CLASSES = (AudienceClaim, IssuedAtClaim, NonceClaim)


def compose_oid4vci_proof_claim_set(*claims: object) -> ClaimSet:
    return ClaimSet(tuple(claims), "oid4vci-proof", CURRENT_VERSION.identifier)


__all__ = ["OID4VCI_PROOF_CLAIM_CLASSES", "compose_oid4vci_proof_claim_set"]
