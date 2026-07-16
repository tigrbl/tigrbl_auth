from tigrbl_sd_jwt_concrete import decode_disclosure, disclosure_digest
from tigrbl_sd_jwt_vc_credential_concrete import SdJwtVcCredential

from .claims import parse_sd_jwt_vc_claims
from .schemas import LEGACY_SD_JWT_VC_TYP, SD_JWT_VC_CARRIER
from .status import parse_status_reference


def validate_sd_jwt_vc(
    credential: SdJwtVcCredential, *, accept_legacy_typ: bool = False
) -> None:
    accepted_types = (
        {SD_JWT_VC_CARRIER.typ, LEGACY_SD_JWT_VC_TYP}
        if accept_legacy_typ
        else {SD_JWT_VC_CARRIER.typ}
    )
    if credential.header.get("typ") not in accepted_types:
        raise ValueError("invalid SD-JWT VC typ")
    parsed = parse_sd_jwt_vc_claims(credential.claims)
    if parsed.status is not None:
        parse_status_reference(parsed.status)
    algorithm = str(credential.claims.get("_sd_alg", "sha-256")).replace("-", "")
    referenced = credential.claims.get("_sd", [])
    if not isinstance(referenced, list) or not all(
        isinstance(item, str) for item in referenced
    ):
        raise ValueError("_sd must be an array")
    seen = set()
    for encoded in credential.disclosures:
        decode_disclosure(encoded)
        digest = disclosure_digest(encoded, algorithm)
        if digest not in referenced or digest in seen:
            raise ValueError("unreferenced or duplicate SD-JWT VC disclosure")
        seen.add(digest)


__all__ = ["validate_sd_jwt_vc"]
