from __future__ import annotations

from dataclasses import dataclass


PUBLIC_CLIENT_FIELDS: tuple[str, ...] = ("name", "client_id", "redirect_uris", "type")
ADMIN_CLIENT_FIELDS: tuple[str, ...] = (
    "id",
    "tenant_id",
    "name",
    "client_id",
    "client_secret",
    "redirect_uris",
    "type",
    "created_at",
    "enabled",
    "policy_tags",
)
DELEGATED_VISIBLE_CLIENT_FIELDS: tuple[str, ...] = (
    "id",
    "tenant_id",
    "name",
    "client_id",
    "redirect_uris",
    "type",
    "created_at",
    "enabled",
)
DELEGATED_MUTABLE_CLIENT_FIELDS: tuple[str, ...] = (
    "name",
    "redirect_uris",
    "enabled",
    "type",
)


@dataclass(frozen=True, slots=True)
class ServiceIdentity:
    service_id: str
    tenant_id: str
    name: str
    scopes: tuple[str, ...]
    enabled: bool = True


@dataclass(frozen=True, slots=True)
class ServiceCredential:
    credential_id: str
    service_id: str
    label: str
    raw_key: str
    created_at: str
    revoked: bool = False
    expires_at: str | None = None


@dataclass(frozen=True, slots=True)
class ServiceIdentityAuthentication:
    service: ServiceIdentity
    credential_id: str
    granted_permissions: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class DelegatedAdminScope:
    subject: str
    tenant_ids: tuple[str, ...]
    permissions: tuple[str, ...]
    visible_client_fields: tuple[str, ...] = DELEGATED_VISIBLE_CLIENT_FIELDS
    mutable_client_fields: tuple[str, ...] = DELEGATED_MUTABLE_CLIENT_FIELDS
    service_identity_permissions: tuple[str, ...] = ()


__all__ = [
    "ADMIN_CLIENT_FIELDS",
    "DELEGATED_MUTABLE_CLIENT_FIELDS",
    "DELEGATED_VISIBLE_CLIENT_FIELDS",
    "DelegatedAdminScope",
    "PUBLIC_CLIENT_FIELDS",
    "ServiceCredential",
    "ServiceIdentity",
    "ServiceIdentityAuthentication",
]
