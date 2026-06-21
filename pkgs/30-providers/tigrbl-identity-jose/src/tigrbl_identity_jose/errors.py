"""JOSE error aliases.

The identity split packages share canonical error classes from
``tigrbl_identity_core`` so compatibility facades and runtime packages catch
the same exception objects.
"""

from __future__ import annotations

from tigrbl_identity_core.errors import InvalidKeyError, InvalidTokenError


__all__ = ["InvalidTokenError", "InvalidKeyError"]
