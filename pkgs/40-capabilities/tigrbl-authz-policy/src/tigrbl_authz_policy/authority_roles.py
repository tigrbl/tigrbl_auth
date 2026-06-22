"""Compatibility re-export for authority role helpers."""

from __future__ import annotations

from .authority import (
    AuthorityRole,
    has_admin_authority,
    has_owner_authority,
    has_superuser_authority,
    normalize_authority_roles,
)

__all__ = [
    "AuthorityRole",
    "has_admin_authority",
    "has_owner_authority",
    "has_superuser_authority",
    "normalize_authority_roles",
]
