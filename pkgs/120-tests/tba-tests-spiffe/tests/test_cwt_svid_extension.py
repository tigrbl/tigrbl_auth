import pytest
from tba_contracts_proof_of_possession import PossessionProofVerificationResult
from tba_profile_workload_credential_cwt_svid_extension import (
    EXPERIMENTAL_EXTENSION,
    SPIFFE_CONFORMANT,
    validate_cwt_svid_extension,
)

VERIFIED_PROOF = PossessionProofVerificationResult(True, replay_accepted=True)
REJECTED_PROOF = PossessionProofVerificationResult(False, replay_accepted=False)


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
