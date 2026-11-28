"""Protocol-neutral current-account self-service contracts."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping


class AccountSelfServiceError(RuntimeError):
    pass


class AccountAuthenticationError(AccountSelfServiceError, PermissionError):
    pass


class AccountNotFoundError(AccountSelfServiceError):
    pass


class AccountValidationError(AccountSelfServiceError, ValueError):
    pass


@dataclass(frozen=True, slots=True)
class AccountPrincipal:
    identity_id: str
    tenant_id: str


@dataclass(frozen=True, slots=True)
class AccountProfile:
    identity_id: str
    tenant_id: str
    username: str
    email: str
    is_active: bool = True
    must_change_password: bool = False
    roles: tuple[str, ...] = ()
    created_at: str | None = None
    updated_at: str | None = None


@dataclass(frozen=True, slots=True)
class AccountProfileUpdate:
    username: str | None = None
    email: str | None = None


@dataclass(frozen=True, slots=True)
class AccountSession:
    session_id: str
    tenant_id: str
    identity_id: str
    username: str
    client_id: str | None = None
    state: str = "active"
    auth_time: str | None = None
    last_seen_at: str | None = None
    expires_at: str | None = None
    ended_at: str | None = None


@dataclass(frozen=True, slots=True)
class AccountConsent:
    consent_id: str
    tenant_id: str
    identity_id: str
    client_id: str
    scope: str
    claims: Mapping[str, Any] | None = None
    state: str = "active"
    granted_at: datetime | None = None
    expires_at: datetime | None = None
    revoked_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class AccountMutation:
    status: str
    resource_id: str | None = None


__all__ = [
    "AccountAuthenticationError",
    "AccountConsent",
    "AccountMutation",
    "AccountNotFoundError",
    "AccountPrincipal",
    "AccountProfile",
    "AccountProfileUpdate",
    "AccountSelfServiceError",
    "AccountSession",
    "AccountValidationError",
]
