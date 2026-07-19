from collections.abc import Mapping
from tigrbl_proof_of_possession_contracts import PossessionProofVerificationResult
from tigrbl_workload_protocol_spiffe_svid import validate_spiffe_id
REQUIRED_CWT_LABELS = frozenset({1, 2, 4, 6, 8})

def validate_cwt_svid_extension(protected_headers: Mapping[object, object], claims: Mapping[int, object], *, proof_result: PossessionProofVerificationResult) -> None:
    if 1 not in protected_headers: raise ValueError("CWT-SVID extension requires protected COSE alg")
    if 4 not in protected_headers: raise ValueError("CWT-SVID extension requires protected COSE kid")
    missing = REQUIRED_CWT_LABELS.difference(claims)
    if missing: raise ValueError(f"missing CWT-SVID extension labels: {sorted(missing)}")
    validate_spiffe_id(str(claims[2]))
    if 3 in claims: raise ValueError("CWT-SVID extension uses a separate audience-bound proof")
    if not isinstance(claims[8], Mapping) or not claims[8]: raise ValueError("CWT-SVID extension requires RFC 8747 cnf")
    if not proof_result.valid or proof_result.replay_accepted is not True:
        raise ValueError("CWT-SVID extension requires verified, replay-accepted proof of possession")