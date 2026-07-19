import pytest
from tigrbl_workload_credential_profile_cwt_svid_extension import EXPERIMENTAL_EXTENSION, SPIFFE_CONFORMANT, validate_cwt_svid_extension
from tigrbl_workload_credential_profile_spiffe_wit_svid import CURRENT_VERSION, validate_wit_svid

def test_wit_svid_is_incubating_and_requires_pop() -> None:
    assert CURRENT_VERSION.status == "Incubating"
    claims = {"iss": "https://issuer", "sub": "spiffe://example.org/w", "cnf": {"jkt": "key"}, "exp": 2}
    validate_wit_svid({"typ": "wit+jwt", "kid": "wit-key", "alg": "ES256"}, claims, proof_verified=True)
    with pytest.raises(ValueError): validate_wit_svid({"typ": "wit+jwt", "kid": "wit-key", "alg": "ES256"}, claims, proof_verified=False)

def test_cwt_svid_is_explicitly_non_spiffe_experimental_extension() -> None:
    assert EXPERIMENTAL_EXTENSION is True and SPIFFE_CONFORMANT is False
    validate_cwt_svid_extension({1: -7, 4: b"kid"}, {1: "issuer", 2: "spiffe://example.org/w", 4: 2, 6: 1, 8: {1: b"key"}}, proof_verified=True)
    with pytest.raises(ValueError): validate_cwt_svid_extension({1: -7, 4: b"kid"}, {1: "issuer", 2: "spiffe://example.org/w", 3: "aud", 4: 2, 6: 1, 8: {1: b"key"}}, proof_verified=True)