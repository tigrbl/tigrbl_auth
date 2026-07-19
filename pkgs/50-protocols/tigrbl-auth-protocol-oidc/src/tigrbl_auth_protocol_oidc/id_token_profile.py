from collections.abc import Mapping, Sequence
from time import time

REQUIRED_ID_TOKEN_CLAIMS = frozenset({"iss", "sub", "aud", "exp", "iat"})


def validate_id_token_profile(
    headers: Mapping[str, object],
    claims: Mapping[str, object],
    *,
    expected_issuer: str,
    client_id: str,
    expected_nonce: str | None = None,
    now: int | None = None,
    clock_skew: int = 0,
    allowed_algorithms: frozenset[str] = frozenset({"RS256"}),
) -> None:
    token_type = headers.get("typ")
    if token_type not in {None, "JWT"}:
        raise ValueError(f"unexpected ID Token type: {token_type}")
    if headers.get("alg") in {None, "none"}:
        raise ValueError("ID Token must use an allowed signing algorithm")
    missing = REQUIRED_ID_TOKEN_CLAIMS.difference(claims)
    if missing:
        raise ValueError(f"missing ID Token claims: {sorted(missing)}")
    if claims["iss"] != expected_issuer:
        raise ValueError("ID Token issuer mismatch")
    subject = claims["sub"]
    if not isinstance(subject, str) or not subject:
        raise ValueError("ID Token subject must be a non-empty string")
    audience = claims["aud"]
    audiences = (
        (audience,)
        if isinstance(audience, str)
        else tuple(audience)
        if isinstance(audience, Sequence)
        else ()
    )
    if client_id not in audiences:
        raise ValueError("ID Token audience mismatch")
    if len(audiences) > 1 and claims.get("azp") != client_id:
        raise ValueError("ID Token azp is required for multiple audiences")
    current = int(time()) if now is None else now
    if (
        not isinstance(claims["exp"], (int, float))
        or current > claims["exp"] + clock_skew
    ):
        raise ValueError("ID Token has expired")
    if (
        not isinstance(claims["iat"], (int, float))
        or claims["iat"] > current + clock_skew
    ):
        raise ValueError("ID Token issued-at time is in the future")
    if expected_nonce is not None and claims.get("nonce") != expected_nonce:
        raise ValueError("ID Token nonce mismatch")
