"""RFC 7519 compact JWT carrier descriptors."""

from dataclasses import dataclass

from tigrbl_identity_contracts.tokens import TokenEnvelopeFormat

from .errors import UnsupportedJwtMediaTypeError


@dataclass(frozen=True, slots=True)
class JwtCarrier:
    media_type: str
    envelope_format: TokenEnvelopeFormat


JWT_CARRIER = JwtCarrier("application/jwt", TokenEnvelopeFormat.JWT)


def select_carrier(media_type: str) -> JwtCarrier:
    if media_type != JWT_CARRIER.media_type:
        raise UnsupportedJwtMediaTypeError(f"unsupported JWT media type: {media_type}")
    return JWT_CARRIER


__all__ = ["JWT_CARRIER", "JwtCarrier", "select_carrier"]
