from typing import Mapping

from .jwk_thumbprints import jwk_thumbprint, verify_jwk_thumbprint


def add_cnf_claim(
    payload: Mapping[str, object], jwk: Mapping[str, object]
) -> dict[str, object]:
    augmented = dict(payload)
    existing = augmented.get("cnf", {})
    if not isinstance(existing, Mapping):
        raise ValueError("cnf must be an object")
    augmented["cnf"] = {**existing, "jkt": jwk_thumbprint(jwk)}
    return augmented


def verify_proof_of_possession(
    payload: Mapping[str, object], jwk: Mapping[str, object]
) -> bool:
    confirmation = payload.get("cnf")
    if not isinstance(confirmation, Mapping) or not isinstance(
        confirmation.get("jkt"), str
    ):
        return False
    return verify_jwk_thumbprint(jwk, confirmation["jkt"])


__all__ = ["add_cnf_claim", "verify_proof_of_possession"]
