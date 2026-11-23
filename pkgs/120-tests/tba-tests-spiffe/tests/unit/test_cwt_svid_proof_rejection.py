import pytest
from tba_contracts_proof_of_possession import PossessionProofVerificationResult
from tba_profile_workload_credential_cwt_svid_extension import (
    validate_cwt_svid_extension,
)


def test_cwt_svid_rejects_unverified_or_replayed_proof() -> None:
    claims = {
        1: "issuer",
        2: "spiffe://example.org/workload",
        4: 200,
        6: 100,
        8: {1: b"key"},
    }
    rejected = PossessionProofVerificationResult(False, replay_accepted=False)
    with pytest.raises(ValueError, match="proof of possession"):
        validate_cwt_svid_extension(
            {1: -7, 4: b"kid"},
            claims,
            proof_result=rejected,
        )
