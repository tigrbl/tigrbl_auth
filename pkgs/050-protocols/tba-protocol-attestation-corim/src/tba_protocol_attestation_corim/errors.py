"""CoRIM protocol/profile mapping errors."""


class CorimProtocolError(ValueError):
    """Base error for a selected CoRIM draft mapping."""


class UnsupportedCorimMediaTypeError(CorimProtocolError):
    """Raised when no selected signed/unsigned CoRIM carrier applies."""


class CorimReferenceIntegrityError(CorimProtocolError):
    """Raised when reference material fails integrity/profile validation."""


__all__ = [
    "CorimProtocolError",
    "CorimReferenceIntegrityError",
    "UnsupportedCorimMediaTypeError",
]
