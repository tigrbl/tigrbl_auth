from tigrbl_identity_contracts.claims import ClaimSet
from tigrbl_audience_claim_concrete import AudienceClaim
from tigrbl_issued_at_claim_concrete import IssuedAtClaim
from tigrbl_issuer_claim_concrete import IssuerClaim
from tigrbl_jwt_id_claim_concrete import JwtIdClaim
from tigrbl_security_events_claim_concrete import SecurityEventsClaim
from tigrbl_subject_claim_concrete import SubjectClaim

SET_CLAIM_CLASSES = (
    IssuerClaim,
    AudienceClaim,
    IssuedAtClaim,
    JwtIdClaim,
    SubjectClaim,
    SecurityEventsClaim,
)


def compose_set_claim_set(*claims) -> ClaimSet:
    required = {"iss", "aud", "iat", "jti", "events"}
    present = {c.name for c in claims}
    missing = required - present
    if missing:
        raise ValueError(f"missing SET claims: {sorted(missing)}")
    return ClaimSet(tuple(claims), "set", "RFC 8417")


__all__ = ["SET_CLAIM_CLASSES", "compose_set_claim_set"]
