"""Authority role helpers owned by the authorization policy boundary."""

from __future__ import annotations

from enum import Enum
from typing import Iterable


class AuthorityRole(str, Enum):
    """Canonical authorization roles for coarse-grained authority checks."""

    ADMIN = "admin"
    OWNER = "owner"
    SUPERUSER = "superuser"


def normalize_authority_roles(values: Iterable[str | AuthorityRole] = ()) -> tuple[str, ...]:
    normalized = {str(value.value if isinstance(value, AuthorityRole) else value).strip() for value in values}
    normalized.discard("")
    return tuple(sorted(normalized))


def has_admin_authority(values: Iterable[str | AuthorityRole] = (), *, principal_kind: str | None = None) -> bool:
    roles = normalize_authority_roles(values)
    return AuthorityRole.ADMIN.value in roles or principal_kind == AuthorityRole.ADMIN.value


def has_owner_authority(values: Iterable[str | AuthorityRole] = ()) -> bool:
    return AuthorityRole.OWNER.value in normalize_authority_roles(values)


def has_superuser_authority(values: Iterable[str | AuthorityRole] = ()) -> bool:
    return AuthorityRole.SUPERUSER.value in normalize_authority_roles(values)


__all__ = [
    "AuthorityRole",
    "has_admin_authority",
    "has_owner_authority",
    "has_superuser_authority",
    "normalize_authority_roles",
]
