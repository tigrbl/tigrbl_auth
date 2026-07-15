import pytest

from tigrbl_auth_protocol_cwt import (
    CAPABILITY_REQUIREMENTS,
    CURRENT_VERSION,
    CWT_CARRIER,
    CWT_REGISTERED_CLAIMS,
    CwtVersion,
    UnsupportedCwtMediaTypeError,
    capability_report,
    compatibility,
    compose_cwt_claim_set,
    migrate_claims,
    select_carrier,
    supports,
)
from tigrbl_claim_cwt_id_concrete import CwtIdClaim
from tigrbl_claim_cwt_issuer_concrete import CwtIssuerClaim
from tigrbl_identity_claims_bases import ClaimBase
from tigrbl_identity_core import ClaimNameKind


def test_cwt_registered_claims_are_standalone_integer_label_objects():
    assert {claim.claim_name for claim in CWT_REGISTERED_CLAIMS} == set(range(1, 8))
    for claim_class in CWT_REGISTERED_CLAIMS:
        assert issubclass(claim_class, ClaimBase)
        claim = (
            claim_class(b"id")
            if claim_class is CwtIdClaim
            else claim_class("aud" if claim_class.claim_name in {1, 2, 3} else 1)
        )
        assert claim.identifier.kind is ClaimNameKind.INTEGER_LABEL
        assert claim.identifier.registry == "IANA CWT Claims"


def test_cwt_claim_set_has_explicit_rfc_version():
    claim_set = compose_cwt_claim_set(CwtIssuerClaim("issuer"))
    assert CURRENT_VERSION is CwtVersion.RFC8392
    assert claim_set.protocol == "cwt"
    assert claim_set.version == "RFC8392"


def test_cwt_owns_revision_features_compatibility_and_migration_entry_point():
    assert supports("cose-protection")
    assert compatibility("RFC8392").compatible
    assert not compatibility("draft-cwt").compatible
    assert migrate_claims({1: "issuer"}, source="RFC8392") == {1: "issuer"}
    with pytest.raises(ValueError, match="unsupported CWT migration"):
        migrate_claims({}, source="draft-cwt")


def test_cwt_owns_carrier_errors_and_explicit_capability_bindings():
    assert select_carrier("application/cwt") is CWT_CARRIER
    with pytest.raises(UnsupportedCwtMediaTypeError):
        select_carrier("application/jwt")

    assert {requirement.operation for requirement in CAPABILITY_REQUIREMENTS} == {
        "decode",
        "encode",
        "validate",
    }
    report = capability_report()
    assert report["selected_revision"] == "RFC8392"
    assert report["required_capabilities"] == ("artifact.processing",)
