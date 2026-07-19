import pytest

from tigrbl_proof_of_possession_contracts import PossessionProofVerificationResult
from tigrbl_workload_credential_profile_cwt_svid_extension import (
    EXPERIMENTAL_EXTENSION,
    SPIFFE_CONFORMANT,
    validate_cwt_svid_extension,
)
from tigrbl_workload_credential_profile_spiffe_wit_svid import (
    CURRENT_VERSION,
    validate_wit_svid,
)


VERIFIED_PROOF = PossessionProofVerificationResult(True, replay_accepted=True)
REJECTED_PROOF = PossessionProofVerificationResult(False, replay_accepted=False)


def test_wit_svid_is_incubating_and_requires_pop() -> None:
    assert CURRENT_VERSION.status == "Incubating"
    claims = {
        "iss": "https://issuer",
        "sub": "spiffe://example.org/w",
        "cnf": {"jkt": "key"},
        "exp": 2,
    }
    headers = {"typ": "wit+jwt", "kid": "wit-key", "alg": "ES256"}
    validate_wit_svid(headers, claims, proof_result=VERIFIED_PROOF)
    with pytest.raises(ValueError):
        validate_wit_svid(headers, claims, proof_result=REJECTED_PROOF)


def test_cwt_svid_is_explicitly_non_spiffe_experimental_extension() -> None:
    assert EXPERIMENTAL_EXTENSION is True and SPIFFE_CONFORMANT is False
    claims = {
        1: "issuer",
        2: "spiffe://example.org/w",
        4: 2,
        6: 1,
        8: {1: b"key"},
    }
    validate_cwt_svid_extension(
        {1: -7, 4: b"kid"},
        claims,
        proof_result=VERIFIED_PROOF,
    )
    with pytest.raises(ValueError):
        validate_cwt_svid_extension(
            {1: -7, 4: b"kid"},
            {**claims, 3: "aud"},
            proof_result=VERIFIED_PROOF,
        )