import pytest
from tigrbl_workload_protocol_spiffe_svid import validate_jwt_svid, validate_spiffe_id, validate_x509_svid

def test_spiffe_id_and_stable_svid_profiles() -> None:
    assert validate_spiffe_id("spiffe://example.org/workload") == ("example.org", "/workload")
    validate_jwt_svid({"alg": "ES256"}, {"sub": "spiffe://example.org/workload", "aud": ["service"], "exp": 2, "iat": 1}, expected_audience="service")
    assert validate_x509_svid(uri_sans=("spiffe://example.org/workload",), dns_sans=(), key_usage_digital_signature=True, basic_constraints_ca=False).startswith("spiffe://")

def test_stable_svid_profiles_reject_wit_semantics_and_bad_names() -> None:
    with pytest.raises(ValueError): validate_spiffe_id("spiffe://example.org/workload/")
    with pytest.raises(ValueError): validate_jwt_svid({"alg": "ES256"}, {"sub": "spiffe://example.org/w", "aud": "a", "exp": 2, "iat": 1, "cnf": {}}, expected_audience="a")