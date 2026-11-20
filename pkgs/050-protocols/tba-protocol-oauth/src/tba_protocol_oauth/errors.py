"""OAuth protocol mapping errors."""


class OAuthProtocolError(RuntimeError):
    """Base error for an OAuth wire or profile failure."""

    def __init__(self, code: str, description: str) -> None:
        super().__init__(description)
        self.code = code
        self.description = description


class UnsupportedOAuthRevisionError(OAuthProtocolError):
    """Raised when an OAuth profile revision has no supported path."""


class OAuthBindingError(OAuthProtocolError):
    """Raised when an OAuth wire element cannot map to a capability."""


__all__ = [
    "OAuthBindingError",
    "OAuthProtocolError",
    "UnsupportedOAuthRevisionError",
]
