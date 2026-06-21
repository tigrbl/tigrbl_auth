"""Delegated administration scope contract dataclasses."""

from __future__ import annotations

from dataclasses import dataclass

from .constants import DELEGATED_MUTABLE_CLIENT_FIELDS, DELEGATED_VISIBLE_CLIENT_FIELDS


@dataclass(frozen=True, slots=True)
class DelegatedAdminScope:
    subject: str
    tenant_ids: tuple[str, ...]
    permissions: tuple[str, ...]
    visible_client_fields: tuple[str, ...] = DELEGATED_VISIBLE_CLIENT_FIELDS
    mutable_client_fields: tuple[str, ...] = DELEGATED_MUTABLE_CLIENT_FIELDS
    service_identity_permissions: tuple[str, ...] = ()


__all__ = ["DelegatedAdminScope"]
