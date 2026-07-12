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


__all__ = [
    "APPLICATION_CWT",
    "APPLICATION_DC_SD_JWT",
    "APPLICATION_EAT_CWT",
    "APPLICATION_EAT_JWT",
    "APPLICATION_VC",
    "APPLICATION_VP",
    "MediaType",
]
