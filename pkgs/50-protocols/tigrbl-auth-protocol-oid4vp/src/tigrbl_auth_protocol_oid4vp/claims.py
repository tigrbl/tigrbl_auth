"""Standalone claim classes used by OID4VP request/proof bindings."""

from tigrbl_claim_client_id_concrete import ClientIdClaim
from tigrbl_claim_nonce_concrete import NonceClaim
from tigrbl_claim_transaction_id_concrete import TransactionIdClaim
from tigrbl_identity_contracts.claims import ClaimSet

from .versions import CURRENT_VERSION

OID4VP_BINDING_CLAIM_CLASSES = (ClientIdClaim, NonceClaim, TransactionIdClaim)


def compose_oid4vp_binding_claim_set(*claims: object) -> ClaimSet:
    return ClaimSet(tuple(claims), "oid4vp-binding", CURRENT_VERSION.identifier)


__all__ = ["OID4VP_BINDING_CLAIM_CLASSES", "compose_oid4vp_binding_claim_set"]
