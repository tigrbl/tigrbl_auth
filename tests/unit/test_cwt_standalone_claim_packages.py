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
    cwt_label_for,
    migrate_claims,
    select_carrier,
    supports,
)
from tigrbl_claim_issuer_concrete import IssuerClaim


def test_cwt_registered_claims_map_integer_labels_to_semantic_claims():
    assert {binding.label for binding in CWT_REGISTERED_CLAIMS} == set(range(1, 8))
    assert {binding.semantic_name for binding in CWT_REGISTERED_CLAIMS} == {
        "iss",
        "sub",
        "aud",
        "exp",
        "nbf",
        "iat",
        "jti",
    }
    assert cwt_label_for(IssuerClaim) == 1
    assert cwt_label_for(IssuerClaim("issuer")) == 1


def test_cwt_claim_set_uses_canonical_claim_objects_and_explicit_rfc_version():
    claim_set = compose_cwt_claim_set(IssuerClaim("issuer"))
    assert CURRENT_VERSION is CwtVersion.RFC8392
    assert claim_set.protocol == "cwt"
    assert claim_set.version == "RFC8392"
    assert isinstance(claim_set.claims[0], IssuerClaim)


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
    assert capability_report()["selected_revision"] == "RFC8392"
