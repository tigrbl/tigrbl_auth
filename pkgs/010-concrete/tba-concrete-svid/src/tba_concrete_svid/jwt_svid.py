from dataclasses import dataclass
from typing import Mapping

from .spiffe_ids import normalize_spiffe_id


@dataclass(frozen=True, slots=True)
class JwtSvidClaimSetPayload:
    subject: str
    audience: tuple[str, ...]
    expiration: int


def parse_jwt_svid_claims(claims: Mapping[str, object]) -> JwtSvidClaimSetPayload:
    subject, audience, expiration = (
        claims.get("sub"),
        claims.get("aud"),
        claims.get("exp"),
    )
    if not isinstance(subject, str):
        raise ValueError("JWT-SVID requires a SPIFFE ID subject")
    normalize_spiffe_id(subject)
    if isinstance(audience, str):
        audience = (audience,)
    elif isinstance(audience, list) and all(isinstance(item, str) for item in audience):
        audience = tuple(audience)
    if not isinstance(audience, tuple) or not audience or not all(audience):
        raise ValueError("JWT-SVID requires a non-empty audience")
    if not isinstance(expiration, int) or isinstance(expiration, bool):
        raise ValueError("JWT-SVID requires NumericDate exp")
    return JwtSvidClaimSetPayload(subject, audience, expiration)


__all__ = ["JwtSvidClaimSetPayload", "parse_jwt_svid_claims"]
