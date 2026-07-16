import base64
import json
from typing import Mapping

from tigrbl_sd_jwt_concrete import parse_sd_jwt_serialization
from tigrbl_sd_jwt_vc_credential_concrete import SdJwtVcCredential


def _decode_object(segment: str) -> Mapping[str, object]:
    try:
        value = json.loads(
            base64.urlsafe_b64decode(segment + "=" * (-len(segment) % 4))
        )
    except (ValueError, UnicodeDecodeError) as exc:
        raise ValueError("invalid SD-JWT VC JSON segment") from exc
    if not isinstance(value, dict):
        raise ValueError("SD-JWT VC segment must be an object")
    return value


def parse_sd_jwt_vc(value: str) -> SdJwtVcCredential:
    serialization = parse_sd_jwt_serialization(value)
    header_segment, claims_segment, _ = serialization.issuer_jwt.split(".")
    return SdJwtVcCredential(
        serialization, _decode_object(header_segment), _decode_object(claims_segment)
    )


__all__ = ["parse_sd_jwt_vc"]
