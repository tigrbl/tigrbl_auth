import hmac
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


def verify_certificate_thumbprint_confirmation(
    payload: Mapping[str, object], presented_thumbprint: str | None
) -> bool:
    """Verify an ``x5t#S256`` confirmation claim without choosing policy."""

    confirmation = payload.get("cnf")
    if not isinstance(confirmation, Mapping):
        return False
    bound = confirmation.get("x5t#S256")
    if not isinstance(bound, str) or not isinstance(presented_thumbprint, str):
        return False
    return hmac.compare_digest(bound, presented_thumbprint)


__all__ = [
    "add_cnf_claim",
    "verify_certificate_thumbprint_confirmation",
    "verify_proof_of_possession",
]
