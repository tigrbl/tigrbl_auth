"""RFC 8392 registered-claim composition."""

from tigrbl_claim_cwt_audience_concrete import CwtAudienceClaim
from tigrbl_claim_cwt_expiration_concrete import CwtExpirationClaim
from tigrbl_claim_cwt_id_concrete import CwtIdClaim
from tigrbl_claim_cwt_issued_at_concrete import CwtIssuedAtClaim
from tigrbl_claim_cwt_issuer_concrete import CwtIssuerClaim
from tigrbl_claim_cwt_not_before_concrete import CwtNotBeforeClaim
from tigrbl_claim_cwt_subject_concrete import CwtSubjectClaim
from tigrbl_identity_contracts.claims import ClaimSet

from .versions import CURRENT_VERSION, CwtVersion

CWT_REGISTERED_CLAIMS = (
    CwtIssuerClaim,
    CwtSubjectClaim,
    CwtAudienceClaim,
    CwtExpirationClaim,
    CwtNotBeforeClaim,
    CwtIssuedAtClaim,
    CwtIdClaim,
)


def compose_cwt_claim_set(
    *claims: object,
    version: CwtVersion = CURRENT_VERSION,
) -> ClaimSet:
    return ClaimSet(tuple(claims), "cwt", version.value)


__all__ = ["CWT_REGISTERED_CLAIMS", "compose_cwt_claim_set"]
