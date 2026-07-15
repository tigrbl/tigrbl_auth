"""RFC 8392 carrier schema descriptors."""

from dataclasses import dataclass

from tigrbl_identity_contracts.tokens import TokenEnvelopeFormat

from .errors import UnsupportedCwtMediaTypeError


@dataclass(frozen=True, slots=True)
class CwtCarrier:
    media_type: str
    envelope_format: TokenEnvelopeFormat


CWT_CARRIER = CwtCarrier("application/cwt", TokenEnvelopeFormat.CWT)


def select_carrier(media_type: str) -> CwtCarrier:
    if media_type != CWT_CARRIER.media_type:
        raise UnsupportedCwtMediaTypeError(f"unsupported CWT media type: {media_type}")
    return CWT_CARRIER


__all__ = ["CWT_CARRIER", "CwtCarrier", "select_carrier"]
