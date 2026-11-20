"""SD-JWT VC profile mapping errors."""


class SdJwtVcProfileError(ValueError):
    """Base error for a selected SD-JWT VC draft mapping."""


class UnsupportedSdJwtVcMediaTypeError(SdJwtVcProfileError):
    """Raised when the current `dc+sd-jwt` carrier is not selected."""


class SdJwtVcKeyBindingError(SdJwtVcProfileError):
    """Raised when required KB-JWT holder binding is absent or invalid."""


__all__ = [
    "SdJwtVcKeyBindingError",
    "SdJwtVcProfileError",
    "UnsupportedSdJwtVcMediaTypeError",
]
