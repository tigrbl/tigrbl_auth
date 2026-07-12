from typing import Mapping

from tigrbl_identity_contracts.attestation import AttestationEvidence

from .claims import EatClaims, EatEncoding, parse_eat_claims


def validate_eat_claims(claims: EatClaims) -> None:
    for nonce in claims.nonce:
        if claims.encoding is EatEncoding.CBOR:
            if not isinstance(nonce, bytes) or not 8 <= len(nonce) <= 64:
                raise ValueError("CBOR EAT nonce must be 8 to 64 bytes")
        elif not isinstance(nonce, str) or not 8 <= len(nonce.encode()) <= 88:
            raise ValueError("JSON EAT nonce must encode to 8 to 88 bytes")
    if claims.ueid is not None:
        length = len(
            claims.ueid if isinstance(claims.ueid, bytes) else claims.ueid.encode()
        )
        if not 7 <= length <= 33:
            raise ValueError("UEID must be 7 to 33 bytes")


def parse_eat(
    claims: Mapping[str | int, object], encoding: EatEncoding | None = None
) -> AttestationEvidence:
    inferred = encoding or (
        EatEncoding.CBOR
        if any(isinstance(name, int) for name in claims)
        else EatEncoding.JSON
    )
    parsed = parse_eat_claims(claims, inferred)
    validate_eat_claims(parsed)
    return AttestationEvidence(str(parsed.profile.identifier), dict(claims))


__all__ = ["parse_eat", "validate_eat_claims"]
