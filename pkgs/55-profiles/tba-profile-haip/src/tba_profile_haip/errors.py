"""HAIP profile composition errors."""


class HaipProfileError(ValueError):
    """Base error for an HAIP configuration or binding failure."""


class HaipComponentVersionError(HaipProfileError):
    """Raised when component protocol revisions are not profile-compatible."""


class HaipTrustBindingError(HaipProfileError):
    """Raised when required wallet/key/verifier trust evidence is unavailable."""


__all__ = ["HaipComponentVersionError", "HaipProfileError", "HaipTrustBindingError"]
