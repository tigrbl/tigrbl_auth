"""RFC 8417 claim-set composition."""

from tigrbl_claim_audience_concrete import AudienceClaim
from tigrbl_claim_issued_at_concrete import IssuedAtClaim
from tigrbl_claim_issuer_concrete import IssuerClaim
from tigrbl_claim_jwt_id_concrete import JwtIdClaim
from tigrbl_claim_security_events_concrete import SecurityEventsClaim
from tigrbl_claim_subject_concrete import SubjectClaim
from tigrbl_identity_contracts.claims import ClaimSet

from .versions import CURRENT_VERSION

SET_CLAIM_CLASSES = (
    IssuerClaim,
    AudienceClaim,
    IssuedAtClaim,
    JwtIdClaim,
    SubjectClaim,
    SecurityEventsClaim,
)


def compose_set_claim_set(*claims: object) -> ClaimSet:
    required = {"iss", "aud", "iat", "jti", "events"}
    present = {claim.name for claim in claims}
    missing = required - present
    if missing:
        raise ValueError(f"missing SET claims: {sorted(missing)}")
    return ClaimSet(tuple(claims), "set", CURRENT_VERSION.identifier)


__all__ = ["SET_CLAIM_CLASSES", "compose_set_claim_set"]
