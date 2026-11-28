"""Standalone claim classes used by OID4VP request/proof bindings."""

from tba_concrete_claim_client_id import ClientIdClaim
from tba_concrete_claim_nonce import NonceClaim
from tba_concrete_claim_transaction_id import TransactionIdClaim
from tba_contracts_identity.claims import ClaimSet

from .versions import CURRENT_VERSION

OID4VP_BINDING_CLAIM_CLASSES = (ClientIdClaim, NonceClaim, TransactionIdClaim)


def compose_oid4vp_binding_claim_set(*claims: object) -> ClaimSet:
    return ClaimSet(tuple(claims), "oid4vp-binding", CURRENT_VERSION.identifier)


__all__ = ["OID4VP_BINDING_CLAIM_CLASSES", "compose_oid4vp_binding_claim_set"]
