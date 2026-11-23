"""Errors raised by the versioned protocol package."""


class ProtocolProfileError(ValueError):
    """The artifact or request does not satisfy the selected protocol profile."""


__all__ = ["ProtocolProfileError"]
