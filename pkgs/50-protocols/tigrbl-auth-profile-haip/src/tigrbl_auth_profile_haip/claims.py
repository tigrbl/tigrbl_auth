"""Claim families composed by HAIP from OID4VCI and OID4VP."""

from tigrbl_auth_protocol_oid4vci.claims import OID4VCI_PROOF_CLAIM_CLASSES
from tigrbl_auth_protocol_oid4vp.claims import OID4VP_BINDING_CLAIM_CLASSES

HAIP_PROOF_CLAIM_CLASSES = tuple(
    dict.fromkeys(OID4VCI_PROOF_CLAIM_CLASSES + OID4VP_BINDING_CLAIM_CLASSES)
)

__all__ = ["HAIP_PROOF_CLAIM_CLASSES"]
