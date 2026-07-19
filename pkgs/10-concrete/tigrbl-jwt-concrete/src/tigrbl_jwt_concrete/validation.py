from collections.abc import Mapping, Sequence
from time import time

def validate_registered_claims(claims: Mapping[str, object], *, issuer: str | None = None, audience: str | None = None, now: int | None = None, clock_skew: int = 0) -> None:
    current = int(time()) if now is None else now
    for name in ("exp", "nbf", "iat"):
        if name in claims and (isinstance(claims[name], bool) or not isinstance(claims[name], (int, float))): raise ValueError(f"JWT {name} must be NumericDate")
    if "exp" in claims and current > float(claims["exp"]) + clock_skew: raise ValueError("JWT expired")
    if "nbf" in claims and current + clock_skew < float(claims["nbf"]): raise ValueError("JWT is not active")
    if "iat" in claims and float(claims["iat"]) > current + clock_skew: raise ValueError("JWT iat is in the future")
    if issuer is not None and claims.get("iss") != issuer: raise ValueError("JWT issuer mismatch")
    if audience is not None:
        presented=claims.get("aud"); values=(presented,) if isinstance(presented, str) else tuple(presented) if isinstance(presented, Sequence) else ()
        if audience not in values: raise ValueError("JWT audience mismatch")