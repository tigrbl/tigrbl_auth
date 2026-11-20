"""Selected SD-JWT VC carrier descriptors."""

from dataclasses import dataclass

from .errors import UnsupportedSdJwtVcMediaTypeError


@dataclass(frozen=True, slots=True)
class SdJwtVcCarrier:
    media_type: str
    typ: str


SD_JWT_VC_CARRIER = SdJwtVcCarrier("application/dc+sd-jwt", "dc+sd-jwt")
LEGACY_SD_JWT_VC_TYP = "vc+sd-jwt"


def select_carrier(media_type: str) -> SdJwtVcCarrier:
    if media_type != SD_JWT_VC_CARRIER.media_type:
        raise UnsupportedSdJwtVcMediaTypeError(
            f"unsupported SD-JWT VC media type: {media_type}"
        )
    return SD_JWT_VC_CARRIER


__all__ = [
    "LEGACY_SD_JWT_VC_TYP",
    "SD_JWT_VC_CARRIER",
    "SdJwtVcCarrier",
    "select_carrier",
]
