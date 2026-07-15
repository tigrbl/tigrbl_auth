"""Neutral tenant-administration call and result contracts."""

from __future__ import annotations

from dataclasses import dataclass


class TenantAdministrationError(RuntimeError):
    """Base tenant-administration use-case error."""


class TenantAdministratorAuthenticationError(TenantAdministrationError):
    """Raised when no authenticated administrator can be resolved."""


class TenantAdministrationConflictError(TenantAdministrationError):
    """Raised when tenant uniqueness constraints would be violated."""


class TenantAdministrationNotFoundError(TenantAdministrationError):
    """Raised when a requested tenant does not exist."""


class TenantAdministrationPolicyError(TenantAdministrationError, PermissionError):
    """Raised when the actor lacks authority for an operation."""


class TenantAdministrationValidationError(TenantAdministrationError, ValueError):
    """Raised when an operation violates a tenant lifecycle invariant."""


@dataclass(frozen=True, slots=True)
class TenantAdministrator:
    actor_id: str
    tenant_id: str
    is_admin: bool = False
    is_superuser: bool = False


@dataclass(frozen=True, slots=True)
class AdminTenant:
    tenant_id: str
    realm_id: str | None
    slug: str
    name: str
    email: str
    is_active: bool = True
    created_at: str | None = None
    updated_at: str | None = None


@dataclass(frozen=True, slots=True)
class AdminTenantCreate:
    realm_id: str | None
    slug: str
    name: str
    email: str


@dataclass(frozen=True, slots=True)
class AdminTenantUpdate:
    realm_id: str | None = None
    slug: str | None = None
    name: str | None = None
    email: str | None = None
    is_active: bool | None = None


__all__ = [
    "AdminTenant",
    "AdminTenantCreate",
    "AdminTenantUpdate",
    "TenantAdministrationConflictError",
    "TenantAdministrationError",
    "TenantAdministrationNotFoundError",
    "TenantAdministrationPolicyError",
    "TenantAdministrationValidationError",
    "TenantAdministrator",
    "TenantAdministratorAuthenticationError",
]
