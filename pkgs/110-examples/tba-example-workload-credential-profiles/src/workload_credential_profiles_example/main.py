from tba_contracts_proof_of_possession import PossessionProofVerificationResult
from tba_profile_workload_credential_spiffe_wit_svid import validate_wit_svid
from tba_profile_workload_credential_wimse_wit import validate_wit
from tba_profile_workload_proof_wimse_wpt import validate_wpt


def run_example() -> tuple[str, ...]:
    wit = {
        "iss": "https://issuer",
        "sub": "spiffe://example.org/workload",
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
        "iat": 1,
    }
    validate_wit({"typ": "wit+jwt", "alg": "ES256"}, wit)
    validate_wit_svid(
        {"typ": "wit+jwt", "alg": "ES256", "kid": "wit-key"},
        wit,
        now=1,
        proof_result=PossessionProofVerificationResult(
            True,
            replay_accepted=True,
        ),
    )
    validate_wpt(
        {"typ": "wpt+jwt", "alg": "ES256"},
        {"aud": "service", "exp": 2, "jti": "proof", "wth": "wit-hash"},
        expected_audience="service",
        expected_wit_hash="wit-hash",
    )
    return ("wit", "wit-svid", "wpt")