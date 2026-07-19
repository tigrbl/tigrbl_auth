from tigrbl_proof_of_possession_contracts import PossessionProofVerificationResult
from tigrbl_workload_credential_profile_spiffe_wit_svid import validate_wit_svid
from tigrbl_workload_credential_profile_wimse_wit import validate_wit
from tigrbl_workload_proof_profile_wimse_wpt import validate_wpt


def run_example() -> tuple[str, ...]:
    wit = {
        "iss": "https://issuer",
        "sub": "spiffe://example.org/workload",
        "cnf": {"jkt": "key"},
        "exp": 2,
        "iat": 1,
    }
    validate_wit({"typ": "wit+jwt", "alg": "ES256"}, wit)
    validate_wit_svid(
        {"typ": "wit+jwt", "alg": "ES256", "kid": "wit-key"},
        wit,
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