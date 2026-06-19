from __future__ import annotations


class ReleaseAssuranceError(ValueError):
    """Raised when a release assurance check fails closed."""


CertificationError = ReleaseAssuranceError


__all__ = ["CertificationError", "ReleaseAssuranceError"]
