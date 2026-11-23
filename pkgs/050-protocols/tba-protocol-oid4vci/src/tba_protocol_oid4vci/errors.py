"""OID4VCI protocol mapping errors."""


class Oid4vciProtocolError(ValueError):
    """Base error for an OID4VCI wire mapping failure."""


class Oid4vciProofError(Oid4vciProtocolError):
    """Raised when a credential request proof cannot be verified or bound."""


class UnsupportedCredentialConfigurationError(Oid4vciProtocolError):
    """Raised when an offered credential configuration is unavailable."""


__all__ = [
    "Oid4vciProofError",
    "Oid4vciProtocolError",
    "UnsupportedCredentialConfigurationError",
]
