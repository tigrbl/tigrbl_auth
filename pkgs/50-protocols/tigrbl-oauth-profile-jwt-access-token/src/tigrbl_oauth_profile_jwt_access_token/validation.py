from collections.abc import Mapping, Sequence
REQUIRED_CLAIMS = frozenset({"iss", "sub", "aud", "exp", "iat", "jti", "client_id"})
def validate_access_token(headers: Mapping[str, object], claims: Mapping[str, object], *, expected_issuer: str, expected_audience: str) -> None:
    if headers.get("typ") != "at+jwt":
        raise ValueError("RFC 9068 access token requires typ=at+jwt")
    if headers.get("alg") in {None, "none"}:
        raise ValueError("RFC 9068 access token must be signed")
    missing = REQUIRED_CLAIMS.difference(claims)
    if missing:
        raise ValueError(f"missing RFC 9068 claims: {sorted(missing)}")
    if claims["iss"] != expected_issuer:
        raise ValueError("access-token issuer mismatch")
    aud = claims["aud"]
    audiences = (aud,) if isinstance(aud, str) else tuple(aud) if isinstance(aud, Sequence) else ()
    if expected_audience not in audiences:
        raise ValueError("access-token audience mismatch")