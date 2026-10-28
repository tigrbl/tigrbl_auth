from collections.abc import Mapping, Sequence

REQUIRED_WPT_CLAIMS = frozenset({"aud", "exp", "jti", "wth"})
OPTIONAL_BINDING_CLAIMS = frozenset({"ath", "tth", "oth"})


def validate_wpt(
    headers: Mapping[str, object],
    claims: Mapping[str, object],
    *,
    expected_audience: str,
    expected_wit_hash: str,
) -> None:
    if headers.get("typ") != "wpt+jwt":
        raise ValueError("WPT requires typ=wpt+jwt")
    if headers.get("alg") in {None, "none"}:
        raise ValueError("WPT must be signed with the WIT confirmation key")
    missing = REQUIRED_WPT_CLAIMS.difference(claims)
    if missing:
        raise ValueError(f"missing WPT claims: {sorted(missing)}")
    aud = claims["aud"]
    audiences = (
        (aud,)
        if isinstance(aud, str)
        else tuple(aud)
        if isinstance(aud, Sequence)
        else ()
    )
    if expected_audience not in audiences:
        raise ValueError("WPT audience mismatch")
    if claims["wth"] != expected_wit_hash:
        raise ValueError("WPT does not bind the presented WIT")
    oth = claims.get("oth", ())
    if not isinstance(oth, (Mapping, Sequence)):
        raise ValueError("WPT oth must contain token hashes")
