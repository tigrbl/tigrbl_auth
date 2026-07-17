from tigrbl_sd_jwt_concrete import decode_disclosure, disclosure_digest

from .claims import parse_sd_jwt_vc_claims
from .status import parse_status_reference
from .types import TYP, SdJwtVc


def validate_sd_jwt_vc(credential: SdJwtVc, *, accept_legacy_typ: bool = False) -> None:
    accepted_types = {TYP, "vc+sd-jwt"} if accept_legacy_typ else {TYP}
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
