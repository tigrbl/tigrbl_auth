"""ISO mdoc protocol errors."""


class IsoMdocProtocolError(ValueError):
    """Raised when an ISO mdoc structure violates the selected revision."""


__all__ = ["IsoMdocProtocolError"]
