"""RFC 7519 registered-claim composition."""

from tba_concrete_claim_audience import AudienceClaim
from tba_concrete_claim_expiration import ExpirationClaim
from tba_concrete_claim_issued_at import IssuedAtClaim
from tba_concrete_claim_issuer import IssuerClaim
from tba_concrete_claim_jwt_id import JwtIdClaim
from tba_concrete_claim_not_before import NotBeforeClaim
from tba_concrete_claim_subject import SubjectClaim
from tba_contracts_identity.claims import ClaimSet

from .versions import CURRENT_VERSION

JWT_VERSION = CURRENT_VERSION.identifier
JWT_CLAIM_CLASSES = (
    IssuerClaim,
    SubjectClaim,
    AudienceClaim,
    ExpirationClaim,
    NotBeforeClaim,
    IssuedAtClaim,
    JwtIdClaim,
)


def compose_jwt_claim_set(*claims: object) -> ClaimSet:
    unexpected = [
        claim.name for claim in claims if not isinstance(claim, JWT_CLAIM_CLASSES)
    ]
    if unexpected:
        raise ValueError(f"claims are not registered by {JWT_VERSION}: {unexpected}")
    return ClaimSet(tuple(claims), "jwt", JWT_VERSION)


__all__ = ["JWT_CLAIM_CLASSES", "JWT_VERSION", "compose_jwt_claim_set"]
