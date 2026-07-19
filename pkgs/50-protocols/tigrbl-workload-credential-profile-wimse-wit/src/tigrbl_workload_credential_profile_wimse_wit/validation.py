from collections.abc import Mapping
REQUIRED_WIT_CLAIMS = frozenset({"iss", "sub", "cnf", "exp", "iat"})
def validate_wit(headers: Mapping[str, object], claims: Mapping[str, object]) -> None:
    if headers.get("typ") != "wit+jwt": raise ValueError("WIT requires typ=wit+jwt")
    if headers.get("alg") in {None, "none"}: raise ValueError("WIT must be signed")
    missing = REQUIRED_WIT_CLAIMS.difference(claims)
    if missing: raise ValueError(f"missing WIT claims: {sorted(missing)}")
    if "aud" in claims: raise ValueError("WIT is presented through a workload proof; aud belongs on the proof")
    if not isinstance(claims["cnf"], Mapping) or not claims["cnf"]: raise ValueError("WIT requires a confirmation key")