from tigrbl_identity_contracts.claims import ClaimSet
from tigrbl_claim_audience_concrete import AudienceClaim
from tigrbl_claim_expiration_concrete import ExpirationClaim
from tigrbl_claim_issued_at_concrete import IssuedAtClaim
from tigrbl_claim_issuer_concrete import IssuerClaim
from tigrbl_claim_jwt_id_concrete import JwtIdClaim
from tigrbl_claim_not_before_concrete import NotBeforeClaim
from tigrbl_claim_subject_concrete import SubjectClaim

from .features import FEATURES_BY_VERSION, supports
from .migrations import migrate_claims
from .versions import CURRENT_VERSION, VERSION_HISTORY, JwtVersion, select_version

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


def compose_jwt_claim_set(*claims) -> ClaimSet:
    unexpected = [
        claim.name for claim in claims if not isinstance(claim, JWT_CLAIM_CLASSES)
    ]
    if unexpected:
        raise ValueError(f"claims are not registered by {JWT_VERSION}: {unexpected}")
    return ClaimSet(tuple(claims), "jwt", JWT_VERSION)


__all__ = [
    "CURRENT_VERSION",
    "FEATURES_BY_VERSION",
    "JWT_CLAIM_CLASSES",
    "JWT_VERSION",
    "VERSION_HISTORY",
    "JwtVersion",
    "compose_jwt_claim_set",
    "migrate_claims",
    "select_version",
    "supports",
]
