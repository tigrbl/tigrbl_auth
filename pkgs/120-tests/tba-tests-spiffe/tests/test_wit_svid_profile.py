import pytest
from tba_contracts_proof_of_possession import PossessionProofVerificationResult
from tba_profile_workload_credential_spiffe_wit_svid import (
    CURRENT_VERSION,
    validate_wit_svid,
)

VERIFIED_PROOF = PossessionProofVerificationResult(True, replay_accepted=True)
REJECTED_PROOF = PossessionProofVerificationResult(False, replay_accepted=False)


WIT_SVID_HEADERS = {"typ": "wit+jwt", "kid": "wit-key", "alg": "ES256"}
WIT_SVID_CLAIMS = {
    "sub": "spiffe://example.org/w",
    "cnf": {
        "jwk": {
            "alg": "ES256",
            "kty": "EC",
            "crv": "P-256",
            "x": "f83OJ3D2xF1Bg8vub9tLe1gHMzV76e8Tus9uPHvRVEU",
            "y": "x_FEzRu9m36HLNFyp2oK5uLrX6FJe2GIhK4tdX7ISJY",
        },
    },
    "exp": 2,
}


@pytest.mark.parametrize("algorithm", ["ES256", "RS256", "PS512"])
def test_wit_svid_is_incubating_and_requires_pop(algorithm) -> None:
    assert CURRENT_VERSION.status == "Incubating"
    headers = {**WIT_SVID_HEADERS, "alg": algorithm}
    validate_wit_svid(headers, WIT_SVID_CLAIMS, proof_result=VERIFIED_PROOF, now=1)
    with pytest.raises(ValueError, match="proof of possession"):
        validate_wit_svid(headers, WIT_SVID_CLAIMS, proof_result=REJECTED_PROOF, now=1)


@pytest.mark.parametrize(
    ("overrides", "message"),
    [
        ({"cnf": {"jkt": "key"}}, "public confirmation JWK"),
        ({"cnf": {"jwk": {"alg": "EdDSA"}}}, "algorithm"),
        ({"cnf": {"jwk": {"alg": "ES256", "d": "private"}}}, "public confirmation JWK"),
        ({"cnf": {"jwk": {"alg": "ES256", "kty": "RSA"}}}, "does not match"),
        ({"exp": 1}, "expired"),
        ({"exp": True}, "NumericDate"),
        ({"nbf": 2}, "not yet valid"),
        ({"aud": "service"}, "must not contain aud"),
    ],
)
def test_wit_svid_rejects_invalid_claims(overrides, message) -> None:
    with pytest.raises(ValueError, match=message):
        validate_wit_svid(
            WIT_SVID_HEADERS,
            {**WIT_SVID_CLAIMS, **overrides},
            proof_result=VERIFIED_PROOF,
            now=1,
        )


def test_wit_svid_rejects_unlisted_header_algorithm() -> None:
    with pytest.raises(ValueError, match="algorithm"):
        validate_wit_svid(
            {**WIT_SVID_HEADERS, "alg": "EdDSA"},
            WIT_SVID_CLAIMS,
            proof_result=VERIFIED_PROOF,
            now=1,
        )
