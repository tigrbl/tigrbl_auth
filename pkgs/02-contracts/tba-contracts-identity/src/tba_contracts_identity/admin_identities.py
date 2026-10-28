"""Neutral identity-administration call and result contracts."""

from __future__ import annotations

from dataclasses import dataclass


class IdentityAdministrationError(RuntimeError):
    pass


class IdentityAdministrationConflictError(IdentityAdministrationError):
    pass


class IdentityAdministrationNotFoundError(IdentityAdministrationError):
    pass


class IdentityAdministrationPolicyError(IdentityAdministrationError, PermissionError):
    pass


class IdentityAdministrationValidationError(IdentityAdministrationError, ValueError):
    pass


@dataclass(frozen=True, slots=True)
class AdminIdentity:
    identity_id: str
    tenant_id: str
    username: str
    email: str
    is_active: bool = True
    is_admin: bool = False
    is_superuser: bool = False
    must_change_password: bool = False
    roles: tuple[str, ...] = ()
    created_at: str | None = None
    updated_at: str | None = None


@dataclass(frozen=True, slots=True)
class AdminIdentityCreate:
    tenant_id: str
    username: str
    email: str
    password: str
    is_admin: bool = False
    is_superuser: bool = False
    must_change_password: bool = True


@dataclass(frozen=True, slots=True)
class AdminIdentityUpdate:
    username: str | None = None
    email: str | None = None
    password: str | None = None
    is_active: bool | None = None
    is_admin: bool | None = None
    is_superuser: bool | None = None
    must_change_password: bool | None = None


__all__ = [
    "AdminIdentity",
    "AdminIdentityCreate",
    "AdminIdentityUpdate",
    "IdentityAdministrationConflictError",
    "IdentityAdministrationError",
    "IdentityAdministrationNotFoundError",
    "IdentityAdministrationPolicyError",
    "IdentityAdministrationValidationError",
]
