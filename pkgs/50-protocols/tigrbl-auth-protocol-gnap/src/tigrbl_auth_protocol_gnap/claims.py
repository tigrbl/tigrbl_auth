"""RFC 9635 subject-information claim composition."""

from tigrbl_claim_assertions_concrete import AssertionsClaim
from tigrbl_claim_subject_identifiers_concrete import SubjectIdentifiersClaim
from tigrbl_claim_updated_at_rfc3339_concrete import UpdatedAtRfc3339Claim
from tigrbl_identity_contracts.claims import ClaimSet

from .versions import CURRENT_VERSION

GNAP_SUBJECT_CLAIM_CLASSES = (
    SubjectIdentifiersClaim,
    AssertionsClaim,
    UpdatedAtRfc3339Claim,
)


def compose_gnap_subject_claim_set(*claims: object) -> ClaimSet:
    unexpected = [
        claim.name
        for claim in claims
        if not isinstance(claim, GNAP_SUBJECT_CLAIM_CLASSES)
    ]
    if unexpected:
        raise ValueError(f"claims are not RFC 9635 subject fields: {unexpected}")
    return ClaimSet(tuple(claims), "gnap-subject", CURRENT_VERSION.identifier)


__all__ = ["GNAP_SUBJECT_CLAIM_CLASSES", "compose_gnap_subject_claim_set"]
