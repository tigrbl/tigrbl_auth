from enum import StrEnum

from tigrbl_claim_cwt_audience_concrete import CwtAudienceClaim
from tigrbl_claim_cwt_expiration_concrete import CwtExpirationClaim
from tigrbl_claim_cwt_id_concrete import CwtIdClaim
from tigrbl_claim_cwt_issued_at_concrete import CwtIssuedAtClaim
from tigrbl_claim_cwt_issuer_concrete import CwtIssuerClaim
from tigrbl_claim_cwt_not_before_concrete import CwtNotBeforeClaim
from tigrbl_claim_cwt_subject_concrete import CwtSubjectClaim
from tigrbl_identity_contracts.claims import ClaimSet
from tigrbl_identity_contracts.protocol_processing import build_protocol_capability_report


class CwtVersion(StrEnum):
    RFC8392 = "RFC8392"


CURRENT_VERSION = CwtVersion.RFC8392
VERSION_HISTORY = (CwtVersion.RFC8392,)
FEATURES_BY_VERSION = {
    CwtVersion.RFC8392.value: frozenset(
        {"registered-claims", "cbor-map", "cose-protection", "application-cwt"}
    )
}
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


def capability_report() -> dict[str, object]:
    return build_protocol_capability_report(
        protocol="cwt",
        revision=CURRENT_VERSION.value,
        features=tuple(FEATURES_BY_VERSION[CURRENT_VERSION.value]),
        evidence_links=("tests/unit/test_claim_object_layers.py",),
    )


__all__ = [
    "CURRENT_VERSION",
    "CWT_REGISTERED_CLAIMS",
    "FEATURES_BY_VERSION",
    "CwtVersion",
    "VERSION_HISTORY",
    "compose_cwt_claim_set",
    "capability_report",
]
