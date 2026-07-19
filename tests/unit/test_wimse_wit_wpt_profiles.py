import pytest
from tigrbl_workload_credential_profile_wimse_wit import CURRENT_VERSION as WIT_VERSION, validate_wit
from tigrbl_workload_proof_profile_wimse_wpt import CURRENT_VERSION as WPT_VERSION, validate_wpt

def test_wit_and_wpt_are_distinct_revision_pinned_artifacts() -> None:
    assert WIT_VERSION.identifier == "draft-ietf-wimse-workload-creds-02"
    assert WPT_VERSION.identifier == "draft-ietf-wimse-wpt-01"
    validate_wit({"typ": "wit+jwt", "alg": "ES256"}, {"iss": "i", "sub": "w", "cnf": {"jkt": "k"}, "exp": 2, "iat": 1})
    validate_wpt({"typ": "wpt+jwt", "alg": "ES256"}, {"aud": "service", "exp": 2, "jti": "p", "wth": "hash", "ath": "access", "tth": "transaction", "oth": ["other"]}, expected_audience="service", expected_wit_hash="hash")

def test_wit_cannot_be_bearer_and_wpt_must_bind_exact_wit() -> None:
    with pytest.raises(ValueError): validate_wit({"typ": "wit+jwt", "alg": "ES256"}, {"iss": "i", "sub": "w", "cnf": {}, "exp": 2, "iat": 1})
    with pytest.raises(ValueError): validate_wpt({"typ": "wpt+jwt", "alg": "ES256"}, {"aud": "service", "exp": 2, "jti": "p", "wth": "wrong"}, expected_audience="service", expected_wit_hash="right")