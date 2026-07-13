import base64
import json
from dataclasses import dataclass
from typing import Mapping

from tigrbl_digital_credential_bases import CredentialFormatBase
from tigrbl_sd_jwt_concrete import SdJwtSerialization, parse_sd_jwt_serialization

DRAFT_REVISION = "draft-ietf-oauth-sd-jwt-vc-17"
MEDIA_TYPE = "application/dc+sd-jwt"
TYP = "dc+sd-jwt"


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


@dataclass(frozen=True, slots=True)
class SdJwtVc(CredentialFormatBase):
    format_identifier = "dc+sd-jwt"
    serialization: SdJwtSerialization
    header: Mapping[str, object]
    claims: Mapping[str, object]

    @property
    def issuer_jwt(self) -> str:
        return self.serialization.issuer_jwt

    @property
    def disclosures(self) -> tuple[str, ...]:
        return self.serialization.disclosures

    @property
    def key_binding_jwt(self) -> str | None:
        return self.serialization.key_binding_jwt


def parse_sd_jwt_vc(value: str) -> SdJwtVc:
    serialization = parse_sd_jwt_serialization(value)
    header_segment, claims_segment, _ = serialization.issuer_jwt.split(".")
    return SdJwtVc(
        serialization, _decode_object(header_segment), _decode_object(claims_segment)
    )


__all__ = ["DRAFT_REVISION", "MEDIA_TYPE", "TYP", "SdJwtVc", "parse_sd_jwt_vc"]
