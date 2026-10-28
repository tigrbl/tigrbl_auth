"""Residency policy errors."""

from __future__ import annotations


class ResidencyPolicyError(PermissionError):
    """Raised when data residency policy denies or cannot evaluate a request."""


__all__ = ["ResidencyPolicyError"]
