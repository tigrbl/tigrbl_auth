import pytest
from tigrbl_credential_profile_vc_jose_cose import CURRENT_VERSION, select_format, validate_cose_vc, validate_jose_vc

def test_vc_jose_cose_is_revision_pinned_and_carriers_are_explicit() -> None:
    assert CURRENT_VERSION.published == "2025-05-15"
    assert select_format("application/vc+jwt").envelope_family == "JOSE"
    assert select_format("application/vc+cose").envelope_family == "COSE"

def test_vc_jose_cose_rejects_carrier_and_artifact_confusion() -> None:
    validate_jose_vc({"alg": "ES256"}, {"credentialSubject": {"id": "did:example:1"}})
    validate_cose_vc({1: -7}, {1: "issuer"})
    with pytest.raises(ValueError): validate_jose_vc({"alg": "ES256"}, {"credentialSubject": {}}, media_type="application/vc+cose")
    with pytest.raises(ValueError): validate_jose_vc({"alg": "none"}, {"credentialSubject": {}})