"""JOSE error aliases.

The identity split packages share canonical error classes from
``tba_primitives_identity`` so compatibility facades and runtime packages catch
the same exception objects.
"""

from __future__ import annotations

from tba_primitives_identity.errors import InvalidKeyError, InvalidTokenError


__all__ = ["InvalidTokenError", "InvalidKeyError"]
