from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True, slots=True)
class KeyBindingClaims:
    audience: str | tuple[str, ...]
    nonce: str
    issued_at: int
    sd_hash: str


def parse_key_binding_claims(claims: Mapping[str, object]) -> KeyBindingClaims:
    audience = claims.get("aud")
    if isinstance(audience, list) and all(isinstance(item, str) for item in audience):
        audience = tuple(audience)
    if not isinstance(audience, (str, tuple)) or not audience:
        raise ValueError("KB-JWT requires aud")
    nonce, issued_at, digest = (
        claims.get("nonce"),
        claims.get("iat"),
        claims.get("sd_hash"),
    )
    if (
        not isinstance(nonce, str)
        or not nonce
        or not isinstance(issued_at, int)
        or isinstance(issued_at, bool)
        or not isinstance(digest, str)
        or not digest
    ):
        raise ValueError("KB-JWT requires nonce, NumericDate iat, and sd_hash")
    return KeyBindingClaims(audience, nonce, issued_at, digest)


__all__ = ["KeyBindingClaims", "parse_key_binding_claims"]
