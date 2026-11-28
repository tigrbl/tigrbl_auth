from collections.abc import Mapping, Sequence
from .spiffe_id import validate_spiffe_id


def validate_jwt_svid(
    headers: Mapping[str, object],
    claims: Mapping[str, object],
    *,
    expected_audience: str,
) -> None:
    if headers.get("alg") in {None, "none"}:
        raise ValueError("JWT-SVID must be signed")
    subject = claims.get("sub")
    if not isinstance(subject, str):
        raise ValueError("JWT-SVID sub is required")
    validate_spiffe_id(subject)
    audience = claims.get("aud")
    values = (
        (audience,)
        if isinstance(audience, str)
        else tuple(audience)
        if isinstance(audience, Sequence)
        else ()
    )
    if expected_audience not in values:
        raise ValueError("JWT-SVID audience mismatch")
    for claim in ("exp", "iat"):
        if not isinstance(claims.get(claim), (int, float)):
            raise ValueError(f"JWT-SVID {claim} is required")
    if "cnf" in claims:
        raise ValueError(
            "JWT-SVID is a bearer credential; use WIT-SVID for mandatory PoP"
        )
