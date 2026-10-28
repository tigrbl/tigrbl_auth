"""Neutral realm-administration call and result contracts."""

from __future__ import annotations

from dataclasses import dataclass


class RealmAdministrationError(RuntimeError):
    pass


class RealmAdministrationConflictError(RealmAdministrationError):
    pass


class RealmAdministrationNotFoundError(RealmAdministrationError):
    pass


class RealmAdministrationValidationError(RealmAdministrationError, ValueError):
    pass


@dataclass(frozen=True, slots=True)
class AdminRealm:
    realm_id: str
    slug: str
    name: str
    issuer_path: str = ""
    description: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


@dataclass(frozen=True, slots=True)
class AdminRealmCreate:
    slug: str
    name: str
    issuer_path: str | None = None
    description: str | None = None


@dataclass(frozen=True, slots=True)
class AdminRealmUpdate:
    slug: str | None = None
    name: str | None = None
    issuer_path: str | None = None
    description: str | None = None


__all__ = [
    "AdminRealm",
    "AdminRealmCreate",
    "AdminRealmUpdate",
    "RealmAdministrationConflictError",
    "RealmAdministrationError",
    "RealmAdministrationNotFoundError",
    "RealmAdministrationValidationError",
]
