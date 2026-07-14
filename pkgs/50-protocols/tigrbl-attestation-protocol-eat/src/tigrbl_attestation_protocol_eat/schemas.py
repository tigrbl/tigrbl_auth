"""RFC 9711 protected-carrier mappings."""

from dataclasses import dataclass

from tigrbl_identity_contracts.tokens import TokenEnvelopeFormat

from .errors import UnsupportedEatCarrierError


@dataclass(frozen=True, slots=True)
class EatCarrier:
    media_type: str
    envelope_format: TokenEnvelopeFormat


EAT_JWT_CARRIER = EatCarrier("application/eat+jwt", TokenEnvelopeFormat.JWT)
EAT_CWT_CARRIER = EatCarrier("application/eat+cwt", TokenEnvelopeFormat.CWT)
EAT_CARRIERS = (EAT_JWT_CARRIER, EAT_CWT_CARRIER)


def select_carrier(media_type: str) -> EatCarrier:
    for carrier in EAT_CARRIERS:
        if carrier.media_type == media_type:
            return carrier
    raise UnsupportedEatCarrierError(f"unsupported EAT media type: {media_type}")


__all__ = [
    "EAT_CARRIERS",
    "EAT_CWT_CARRIER",
    "EAT_JWT_CARRIER",
    "EatCarrier",
    "select_carrier",
]
