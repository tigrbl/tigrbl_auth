from collections.abc import Mapping
from tigrbl_proof_of_possession_contracts import PossessionProofVerificationResult
from tigrbl_workload_protocol_spiffe_svid import validate_spiffe_id
ALLOWED_ALGORITHMS = frozenset({"ES256", "ES384", "ES512", "EdDSA"})

def validate_wit_svid(headers: Mapping[str, object], claims: Mapping[str, object], *, proof_result: PossessionProofVerificationResult) -> None:
    if headers.get("typ") != "wit+jwt": raise ValueError("WIT-SVID requires typ=wit+jwt")
    if not isinstance(headers.get("kid"), str) or not headers["kid"]: raise ValueError("WIT-SVID requires kid")
    if headers.get("alg") not in ALLOWED_ALGORITHMS: raise ValueError("WIT-SVID algorithm is not permitted")
    missing = {"iss", "sub", "cnf", "exp"}.difference(claims)
    if missing: raise ValueError(f"missing WIT-SVID claims: {sorted(missing)}")
    validate_spiffe_id(str(claims["sub"]))
    if "aud" in claims: raise ValueError("WIT-SVID must not contain aud")
    if not isinstance(claims["cnf"], Mapping) or not claims["cnf"]: raise ValueError("WIT-SVID requires confirmation key")
    if not proof_result.valid or proof_result.replay_accepted is not True:
        raise ValueError("WIT-SVID requires verified, replay-accepted proof of possession")