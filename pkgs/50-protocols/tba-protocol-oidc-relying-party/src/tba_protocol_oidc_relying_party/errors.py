"""RP protocol mapping errors."""


class RPError(RuntimeError):
    """Raised when the RP cannot safely process a protocol interaction."""


class UnsupportedRpProfileError(RPError):
    """Raised when no compatibility path exists for a selected RP profile."""


__all__ = ["RPError", "UnsupportedRpProfileError"]
