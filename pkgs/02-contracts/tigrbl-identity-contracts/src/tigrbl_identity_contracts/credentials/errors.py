"""Credential contract errors."""

from __future__ import annotations


class CredentialError(Exception):
    """Base credential lifecycle error."""


class CredentialVerificationError(CredentialError):
    """Raised when presented credential material does not verify."""


class CredentialStateError(CredentialError):
    """Raised when a credential is not usable in its current lifecycle state."""


__all__ = ["CredentialError", "CredentialStateError", "CredentialVerificationError"]
