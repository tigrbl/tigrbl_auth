"""RFC 8392 integer-label mappings for canonical semantic claims."""

from dataclasses import dataclass
from typing import TypeAlias

from tba_concrete_claim_audience import AudienceClaim
from tba_bases_claim import ClaimBase
from tba_concrete_claim_expiration import ExpirationClaim
from tba_concrete_claim_issued_at import IssuedAtClaim
from tba_concrete_claim_issuer import IssuerClaim
from tba_concrete_claim_jwt_id import JwtIdClaim
from tba_concrete_claim_not_before import NotBeforeClaim
from tba_concrete_claim_subject import SubjectClaim
from tba_contracts_identity.claims import ClaimSet

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
