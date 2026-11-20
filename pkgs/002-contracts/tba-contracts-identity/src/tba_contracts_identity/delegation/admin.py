"""Delegated administration contract dataclasses and client-field constants."""

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
]
