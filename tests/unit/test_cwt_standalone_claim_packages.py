from tigrbl_auth_protocol_cwt import (
    CURRENT_VERSION,
    CWT_REGISTERED_CLAIMS,
    CwtVersion,
    compose_cwt_claim_set,
)
from tigrbl_claim_cwt_id_concrete import CwtIdClaim
from tigrbl_claim_cwt_issuer_concrete import CwtIssuerClaim
from tigrbl_identity_claims_bases import ClaimBase
from tigrbl_identity_core import ClaimNameKind


def test_cwt_registered_claims_are_standalone_integer_label_objects():
    assert {claim.claim_name for claim in CWT_REGISTERED_CLAIMS} == set(range(1, 8))
    for claim_class in CWT_REGISTERED_CLAIMS:
        assert issubclass(claim_class, ClaimBase)
        claim = claim_class(b"id") if claim_class is CwtIdClaim else claim_class(
            "aud" if claim_class.claim_name in {1, 2, 3} else 1
        )
        assert claim.identifier.kind is ClaimNameKind.INTEGER_LABEL
        assert claim.identifier.registry == "IANA CWT Claims"


def test_cwt_claim_set_has_explicit_rfc_version():
    claim_set = compose_cwt_claim_set(CwtIssuerClaim("issuer"))
    assert CURRENT_VERSION is CwtVersion.RFC8392
    assert claim_set.protocol == "cwt"
    assert claim_set.version == "RFC8392"
