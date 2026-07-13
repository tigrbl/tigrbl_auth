from tigrbl_identity_contracts.claims import ClaimSet
from tigrbl_claim_audience_concrete import AudienceClaim
from tigrbl_claim_issued_at_concrete import IssuedAtClaim
from tigrbl_claim_issuer_concrete import IssuerClaim
from tigrbl_claim_jwt_id_concrete import JwtIdClaim
from tigrbl_claim_security_events_concrete import SecurityEventsClaim
from tigrbl_claim_subject_concrete import SubjectClaim

from .features import FEATURES_BY_VERSION, supports
from .migrations import migrate_claims
from .versions import CURRENT_VERSION, VERSION_HISTORY, SetVersion, select_version

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
    return ClaimSet(tuple(claims), "set", "RFC8417")


__all__ = [
    "CURRENT_VERSION",
    "FEATURES_BY_VERSION",
    "SET_CLAIM_CLASSES",
    "VERSION_HISTORY",
    "SetVersion",
    "compose_set_claim_set",
    "migrate_claims",
    "select_version",
    "supports",
]
