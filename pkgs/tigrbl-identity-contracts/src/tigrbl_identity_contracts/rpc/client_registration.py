"""Schemas for dynamic client registration admin methods."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from .common import PaginationParams
from tigrbl_auth.api.rpc.registry import RpcSchema


class ClientRegistrationRecord(RpcSchema):
    id: str
    client_id: str
    tenant_id: str | None = None
    software_id: str | None = None
    software_version: str | None = None
    contacts: list[str] = Field(default_factory=list)
    registration_client_uri: str | None = None
    registration_access_token_hash: str | None = None
    issued_at: str | None = None
    rotated_at: str | None = None
    disabled_at: str | None = None
    registration_metadata: dict[str, Any] = Field(default_factory=dict)


class ClientRegistrationListParams(PaginationParams):
    client_id: str | None = None
    tenant_id: str | None = None


class ClientRegistrationListResult(RpcSchema):
    count: int
    items: list[ClientRegistrationRecord] = Field(default_factory=list)


class ClientRegistrationShowParams(RpcSchema):
    client_id: str


class ClientRegistrationShowResult(RpcSchema):
    registration: ClientRegistrationRecord | None = None


class ClientRegistrationUpsertParams(RpcSchema):
    client_id: str
    tenant_id: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    contacts: list[str] = Field(default_factory=list)
    software_id: str | None = None
    software_version: str | None = None
    registration_access_token_hash: str | None = None
    registration_client_uri: str | None = None


class ClientRegistrationUpsertResult(RpcSchema):
    registration: ClientRegistrationRecord


class ClientRegistrationDeleteParams(RpcSchema):
    client_id: str
    if_missing: str = 'error'


class ClientRegistrationDeleteResult(RpcSchema):
    deleted: bool
    registration: ClientRegistrationRecord | None = None
    status: str


__all__ = [
    'ClientRegistrationDeleteParams',
    'ClientRegistrationDeleteResult',
    'ClientRegistrationListParams',
    'ClientRegistrationListResult',
    'ClientRegistrationRecord',
    'ClientRegistrationShowParams',
    'ClientRegistrationShowResult',
    'ClientRegistrationUpsertParams',
    'ClientRegistrationUpsertResult',
]
