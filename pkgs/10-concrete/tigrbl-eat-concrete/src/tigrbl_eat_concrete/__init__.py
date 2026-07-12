from typing import Any, Mapping
from tigrbl_identity_contracts.attestation import AttestationEvidence

EAT_PROFILE_CLAIM = 265
EAT_NONCE_CLAIM = 10


def parse_eat(claims: Mapping[str | int, Any]) -> AttestationEvidence:
    profile = claims.get(EAT_PROFILE_CLAIM, claims.get("eat_profile"))
    if not isinstance(profile, (str, int)):
        raise ValueError("EAT requires an eat_profile claim")
    nonce = claims.get(EAT_NONCE_CLAIM, claims.get("nonce"))
    if nonce is not None and not isinstance(nonce, (bytes, str, list)):
        raise ValueError("EAT nonce has an invalid representation")
    return AttestationEvidence(str(profile), dict(claims))


__all__ = ["EAT_NONCE_CLAIM", "EAT_PROFILE_CLAIM", "parse_eat"]
