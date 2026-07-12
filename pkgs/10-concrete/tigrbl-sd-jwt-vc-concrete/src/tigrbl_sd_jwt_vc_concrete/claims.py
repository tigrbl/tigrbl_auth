from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True, slots=True)
class SdJwtVcClaims:
    credential_type: str
    issuer: str | None = None
    issued_at: int | None = None
    not_before: int | None = None
    expiration: int | None = None
    confirmation: Mapping[str, object] | None = None
    status: Mapping[str, object] | None = None
    type_integrity: str | None = None


def parse_sd_jwt_vc_claims(claims: Mapping[str, object]) -> SdJwtVcClaims:
    credential_type = claims.get("vct")
    if not isinstance(credential_type, str) or not credential_type:
        raise ValueError("SD-JWT VC requires a non-empty vct claim")
    for name in ("iat", "nbf", "exp"):
        value = claims.get(name)
        if value is not None and (
            not isinstance(value, int) or isinstance(value, bool)
        ):
            raise ValueError(f"{name} must be a NumericDate")
    for name in ("cnf", "status"):
        if name in claims and not isinstance(claims[name], Mapping):
            raise ValueError(f"{name} must be an object")
    integrity = claims.get("vct#integrity")
    if integrity is not None and (not isinstance(integrity, str) or not integrity):
        raise ValueError("vct#integrity must be an integrity metadata string")
    return SdJwtVcClaims(
        credential_type,
        claims.get("iss") if isinstance(claims.get("iss"), str) else None,
        claims.get("iat"),
        claims.get("nbf"),
        claims.get("exp"),
        claims.get("cnf"),
        claims.get("status"),
        integrity,
    )


__all__ = ["SdJwtVcClaims", "parse_sd_jwt_vc_claims"]
