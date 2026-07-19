"""Deterministic RFC 7519 structural values."""

from dataclasses import dataclass
import json
from typing import Mapping

from tigrbl_jws_concrete import JwsCompact, parse_jws_compact

from .validation import validate_registered_claims


@dataclass(frozen=True, slots=True)
class JwtObject:
    serialized: str
    jws: JwsCompact
    claims: Mapping[str, object]
    integrity_verified: bool = False


def decode_jwt_unverified(value: str) -> JwtObject:
    jws = parse_jws_compact(value)
    if jws.payload is None:
        raise ValueError("JWT payload must not be detached")
    try:
        claims = json.loads(jws.payload)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ValueError("JWT claims must be a UTF-8 JSON object") from exc
    if not isinstance(claims, dict):
        raise ValueError("JWT claims must be a JSON object")
    return JwtObject(value, jws, claims)


__all__ = ["JwtObject", "decode_jwt_unverified", "validate_registered_claims"]
