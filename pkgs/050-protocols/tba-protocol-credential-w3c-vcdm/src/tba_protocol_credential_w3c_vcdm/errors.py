"""W3C VCDM protocol errors."""


class VcdmProtocolError(ValueError):
    """Raised when a VCDM document violates the selected recommendation."""


__all__ = ["VcdmProtocolError"]
