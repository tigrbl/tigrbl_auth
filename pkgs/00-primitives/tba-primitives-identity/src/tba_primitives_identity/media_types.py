"""Small, strict media-type value objects."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MediaType:
    value: str

    def __post_init__(self) -> None:
        value = str(self.value).strip().lower()
        if "/" not in value or any(char.isspace() for char in value):
            raise ValueError("media type must be a type/subtype value")
        object.__setattr__(self, "value", value)

    def __str__(self) -> str:
        return self.value


APPLICATION_DC_SD_JWT = MediaType("application/dc+sd-jwt")
APPLICATION_VC = MediaType("application/vc")
APPLICATION_VP = MediaType("application/vp")
APPLICATION_CWT = MediaType("application/cwt")
APPLICATION_EAT_JWT = MediaType("application/eat+jwt")
APPLICATION_EAT_CWT = MediaType("application/eat+cwt")
APPLICATION_JWT = MediaType("application/jwt")
APPLICATION_AT_JWT = MediaType("application/at+jwt")
APPLICATION_WIT_JWT = MediaType("application/wit+jwt")
APPLICATION_WPT_JWT = MediaType("application/wpt+jwt")
APPLICATION_VC_JWT = MediaType("application/vc+jwt")
APPLICATION_VP_JWT = MediaType("application/vp+jwt")
APPLICATION_VC_COSE = MediaType("application/vc+cose")
APPLICATION_VP_COSE = MediaType("application/vp+cose")
APPLICATION_COSE = MediaType("application/cose")
APPLICATION_DID_JSON = MediaType("application/did+json")
APPLICATION_DID_LD_JSON = MediaType("application/did+ld+json")


__all__ = [
    "APPLICATION_CWT",
    "APPLICATION_DC_SD_JWT",
    "APPLICATION_EAT_CWT",
    "APPLICATION_EAT_JWT",
    "APPLICATION_JWT",
    "APPLICATION_AT_JWT",
    "APPLICATION_WIT_JWT",
    "APPLICATION_WPT_JWT",
    "APPLICATION_VC_JWT",
    "APPLICATION_VP_JWT",
    "APPLICATION_VC_COSE",
    "APPLICATION_VP_COSE",
    "APPLICATION_COSE",
    "APPLICATION_DID_JSON",
    "APPLICATION_DID_LD_JSON",
    "APPLICATION_VC",
    "APPLICATION_VP",
    "MediaType",
]
