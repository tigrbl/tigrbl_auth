"""EAT protocol mapping errors."""


class EatProtocolError(ValueError):
    """Base error for an RFC 9711 mapping failure."""


class UnsupportedEatCarrierError(EatProtocolError):
    """Raised when neither the EAT JWT nor EAT CWT carrier applies."""


class EatProfileBindingError(EatProtocolError):
    """Raised when the authenticated profile and evidence profile differ."""


__all__ = [
    "EatProfileBindingError",
    "EatProtocolError",
    "UnsupportedEatCarrierError",
]
