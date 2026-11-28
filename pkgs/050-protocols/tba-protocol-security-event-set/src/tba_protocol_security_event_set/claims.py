"""RFC 8417 claim-set composition."""

from tba_concrete_claim_audience import AudienceClaim
from tba_concrete_claim_issued_at import IssuedAtClaim
from tba_concrete_claim_issuer import IssuerClaim
from tba_concrete_claim_jwt_id import JwtIdClaim
from tba_concrete_claim_security_events import SecurityEventsClaim
from tba_concrete_claim_subject import SubjectClaim
from tba_contracts_identity.claims import ClaimSet

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
