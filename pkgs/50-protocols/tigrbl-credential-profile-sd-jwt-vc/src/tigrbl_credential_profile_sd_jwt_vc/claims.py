"""SD-JWT VC claim-set composition."""

from dataclasses import dataclass
from typing import Mapping

from tigrbl_claim_credential_status_concrete import CredentialStatusClaim
from tigrbl_claim_credential_type_concrete import CredentialTypeClaim
from tigrbl_identity_contracts.claims import ClaimSet

from .versions import CURRENT_VERSION

SD_JWT_VC_CLAIM_CLASSES = (CredentialTypeClaim, CredentialStatusClaim)


@dataclass(frozen=True, slots=True)
class SdJwtVcClaimSetPayload:
    credential_type: str
    issuer: str | None = None
    issued_at: int | None = None
    not_before: int | None = None
    expiration: int | None = None
    confirmation: Mapping[str, object] | None = None
    status: Mapping[str, object] | None = None
    type_integrity: str | None = None


def parse_sd_jwt_vc_claims(claims: Mapping[str, object]) -> SdJwtVcClaimSetPayload:
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
    return SdJwtVcClaimSetPayload(
        credential_type,
        claims.get("iss") if isinstance(claims.get("iss"), str) else None,
        claims.get("iat"),
        claims.get("nbf"),
        claims.get("exp"),
        claims.get("cnf"),
        claims.get("status"),
        integrity,
    )


def compose_sd_jwt_vc_claim_set(*claims: object) -> ClaimSet:
    if not any(isinstance(claim, CredentialTypeClaim) for claim in claims):
        raise ValueError("SD-JWT VC requires vct")
    return ClaimSet(tuple(claims), "sd-jwt-vc", CURRENT_VERSION.identifier)


__all__ = [
    "SD_JWT_VC_CLAIM_CLASSES",
    "SdJwtVcClaimSetPayload",
    "compose_sd_jwt_vc_claim_set",
    "parse_sd_jwt_vc_claims",
]
