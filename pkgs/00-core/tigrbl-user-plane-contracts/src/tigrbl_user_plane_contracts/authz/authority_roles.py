"""Authority role helpers owned by the authorization policy boundary."""

from __future__ import annotations

from enum import Enum


class AuthorityRole(str, Enum):
    """Canonical authorization roles for coarse-grained authority checks."""

    ADMIN = "admin"
    OWNER = "owner"
    SUPERUSER = "superuser"


__all__ = [
    "AuthorityRole",
]
