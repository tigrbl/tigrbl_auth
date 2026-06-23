"""Authority role helpers owned by the authorization policy boundary."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AuthorityRole(str, Enum):
    """Canonical authorization roles for coarse-grained authority checks."""

    ADMIN = "admin"
    OWNER = "owner"
    SUPERUSER = "superuser"


@dataclass(frozen=True, slots=True)
class Role:
    name: str
    permissions: tuple[str, ...]
    tenant_id: str | None = None
    denied_permissions: tuple[str, ...] = ()
    inherited_roles: tuple[str, ...] = ()


__all__ = [
    "AuthorityRole",
    "Role",
]
