"""CoRIM family carrier descriptors."""

from dataclasses import dataclass

from .errors import UnsupportedCorimMediaTypeError


@dataclass(frozen=True, slots=True)
class CorimCarrier:
    media_type: str
    signed: bool


CORIM_UNSIGNED_CARRIER = CorimCarrier("application/corim-unsigned+cbor", False)
CORIM_SIGNED_CARRIER = CorimCarrier("application/corim-signed+cbor", True)
CORIM_CARRIERS = (CORIM_UNSIGNED_CARRIER, CORIM_SIGNED_CARRIER)


def select_carrier(media_type: str) -> CorimCarrier:
    for carrier in CORIM_CARRIERS:
        if carrier.media_type == media_type:
            return carrier
    raise UnsupportedCorimMediaTypeError(f"unsupported CoRIM media type: {media_type}")


__all__ = [
    "CORIM_CARRIERS",
    "CORIM_SIGNED_CARRIER",
    "CORIM_UNSIGNED_CARRIER",
    "CorimCarrier",
    "select_carrier",
]
