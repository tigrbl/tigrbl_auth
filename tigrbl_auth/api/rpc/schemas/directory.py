"""Schemas for directory-style admin lookups."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from .common import PaginationParams
from tigrbl_auth.api.rpc.registry import RpcSchema


class TenantRecord(RpcSchema):
    id: str
    name: str | None = None
    email: str | None = None
    slug: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class TenantListParams(PaginationParams):
    pass


class TenantListResult(RpcSchema):
    count: int
    items: list[TenantRecord] = Field(default_factory=list)


class TenantShowParams(RpcSchema):
    id: str


class TenantShowResult(RpcSchema):
    tenant: TenantRecord | None = None


class ClientRecord(RpcSchema):
    id: str
    tenant_id: str | None = None
    redirect_uris: str | None = None
    grant_types: str | None = None
    response_types: str | None = None
    active: bool | None = None
    created_at: str | None = None
    updated_at: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class ClientListParams(PaginationParams):
    tenant_id: str | None = None


class ClientListResult(RpcSchema):
    count: int
    items: list[ClientRecord] = Field(default_factory=list)


class ClientShowParams(RpcSchema):
    id: str


class ClientShowResult(RpcSchema):
    client: ClientRecord | None = None


class IdentityRecord(RpcSchema):
    id: str
    tenant_id: str | None = None
    username: str | None = None
    email: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class IdentityListParams(PaginationParams):
    tenant_id: str | None = None


class IdentityListResult(RpcSchema):
    count: int
    items: list[IdentityRecord] = Field(default_factory=list)


class IdentityShowParams(RpcSchema):
    id: str


class IdentityShowResult(RpcSchema):
    identity: IdentityRecord | None = None


__all__ = [
    "ClientListParams",
    "ClientListResult",
    "ClientRecord",
    "ClientShowParams",
    "ClientShowResult",
    "IdentityListParams",
    "IdentityListResult",
    "IdentityRecord",
    "IdentityShowParams",
    "IdentityShowResult",
    "TenantListParams",
    "TenantListResult",
    "TenantRecord",
    "TenantShowParams",
    "TenantShowResult",
]
