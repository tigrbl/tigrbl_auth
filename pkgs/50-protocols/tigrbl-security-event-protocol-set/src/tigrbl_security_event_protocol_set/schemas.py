"""RFC 8417 protected-carrier descriptor."""

from dataclasses import dataclass

from tigrbl_identity_contracts.tokens import TokenEnvelopeFormat

from .errors import UnsupportedSetMediaTypeError


@dataclass(frozen=True, slots=True)
class SetCarrier:
    media_type: str
    envelope_format: TokenEnvelopeFormat


SET_JWT_CARRIER = SetCarrier(
    "application/secevent+jwt",
    TokenEnvelopeFormat.JWT,
)


def select_carrier(media_type: str) -> SetCarrier:
    if media_type != SET_JWT_CARRIER.media_type:
        raise UnsupportedSetMediaTypeError(f"unsupported SET media type: {media_type}")
    return SET_JWT_CARRIER


__all__ = ["SET_JWT_CARRIER", "SetCarrier", "select_carrier"]
