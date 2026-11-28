"""OID4VP protocol mapping errors."""


class Oid4vpProtocolError(ValueError):
    """Base error for an OID4VP wire mapping failure."""


class Oid4vpRequestBindingError(Oid4vpProtocolError):
    """Raised when client/nonce/transaction binding cannot be established."""


class UnsupportedPresentationFormatError(Oid4vpProtocolError):
    """Raised when no accepted presentation format can be selected."""


__all__ = [
    "Oid4vpProtocolError",
    "Oid4vpRequestBindingError",
    "UnsupportedPresentationFormatError",
]
