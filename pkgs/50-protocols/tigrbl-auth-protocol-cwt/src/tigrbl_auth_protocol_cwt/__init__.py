from enum import StrEnum

from tigrbl_claim_cwt_audience_concrete import CwtAudienceClaim
from tigrbl_claim_cwt_expiration_concrete import CwtExpirationClaim
from tigrbl_claim_cwt_id_concrete import CwtIdClaim
from tigrbl_claim_cwt_issued_at_concrete import CwtIssuedAtClaim
from tigrbl_claim_cwt_issuer_concrete import CwtIssuerClaim
from tigrbl_claim_cwt_not_before_concrete import CwtNotBeforeClaim
from tigrbl_claim_cwt_subject_concrete import CwtSubjectClaim
from tigrbl_identity_contracts.claims import ClaimSet


class CwtVersion(StrEnum):
    RFC8392 = "RFC8392"


CURRENT_VERSION = CwtVersion.RFC8392
VERSION_HISTORY = (CwtVersion.RFC8392,)
CWT_REGISTERED_CLAIMS = (
    CwtIssuerClaim,
    CwtSubjectClaim,
    CwtAudienceClaim,
    CwtExpirationClaim,
    CwtNotBeforeClaim,
    CwtIssuedAtClaim,
    CwtIdClaim,
)


def compose_cwt_claim_set(*claims, version: CwtVersion = CURRENT_VERSION) -> ClaimSet:
    return ClaimSet(tuple(claims), "cwt", version.value)


__all__ = [
    "CURRENT_VERSION",
    "CWT_REGISTERED_CLAIMS",
    "CwtVersion",
    "VERSION_HISTORY",
    "compose_cwt_claim_set",
]
