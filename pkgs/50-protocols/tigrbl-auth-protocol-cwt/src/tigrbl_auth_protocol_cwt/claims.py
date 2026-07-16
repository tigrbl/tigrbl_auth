"""RFC 8392 integer-label mappings for canonical semantic claims."""

from dataclasses import dataclass
from typing import TypeAlias

from tigrbl_claim_audience_concrete import AudienceClaim
from tigrbl_claim_bases import ClaimBase
from tigrbl_claim_expiration_concrete import ExpirationClaim
from tigrbl_claim_issued_at_concrete import IssuedAtClaim
from tigrbl_claim_issuer_concrete import IssuerClaim
from tigrbl_claim_jwt_id_concrete import JwtIdClaim
from tigrbl_claim_not_before_concrete import NotBeforeClaim
from tigrbl_claim_subject_concrete import SubjectClaim
from tigrbl_identity_contracts.claims import ClaimSet

from .versions import CURRENT_VERSION, CwtVersion


ClaimClass: TypeAlias = type[ClaimBase]


@dataclass(frozen=True, slots=True)
class CwtClaimBinding:
    label: int
    claim_class: ClaimClass

    @property
    def semantic_name(self) -> str:
        return str(self.claim_class.claim_name)


CWT_REGISTERED_CLAIMS = (
    CwtClaimBinding(1, IssuerClaim),
    CwtClaimBinding(2, SubjectClaim),
    CwtClaimBinding(3, AudienceClaim),
    CwtClaimBinding(4, ExpirationClaim),
    CwtClaimBinding(5, NotBeforeClaim),
    CwtClaimBinding(6, IssuedAtClaim),
    CwtClaimBinding(7, JwtIdClaim),
)
CWT_LABEL_BY_CLAIM = {
    binding.claim_class: binding.label for binding in CWT_REGISTERED_CLAIMS
}
CWT_CLAIM_BY_LABEL = {
    binding.label: binding.claim_class for binding in CWT_REGISTERED_CLAIMS
}


def compose_cwt_claim_set(
    *claims: ClaimBase,
    version: CwtVersion = CURRENT_VERSION,
) -> ClaimSet:
    return ClaimSet(tuple(claims), "cwt", version.value)


def cwt_label_for(claim: ClaimBase | ClaimClass) -> int:
    claim_class = claim if isinstance(claim, type) else type(claim)
    try:
        return CWT_LABEL_BY_CLAIM[claim_class]
    except KeyError as exc:
        raise ValueError(
            f"claim is not registered by CWT: {claim_class.__name__}"
        ) from exc


__all__ = [
    "CWT_CLAIM_BY_LABEL",
    "CWT_LABEL_BY_CLAIM",
    "CWT_REGISTERED_CLAIMS",
    "CwtClaimBinding",
    "compose_cwt_claim_set",
    "cwt_label_for",
]
