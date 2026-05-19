"""Schemas for token inspection RPC methods."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from .common import PaginationParams
from tigrbl_auth.api.rpc.registry import RpcSchema


class TokenRecordView(RpcSchema):
    id: str | None = None
    token_hash: str
    token_kind: str | None = None
    token_type_hint: str | None = None
    active: bool
    subject: str | None = None
    tenant_id: str | None = None
    client_id: str | None = None
    scope: str | None = None
    issuer: str | None = None
    audience: Any = None
    issued_at: str | None = None
    expires_at: str | None = None
    revoked_at: str | None = None
    revoked_reason: str | None = None
    claims: dict[str, Any] = Field(default_factory=dict)


class TokenListParams(PaginationParams):
    active_only: bool = False
    subject: str | None = None
    client_id: str | None = None


class TokenListResult(RpcSchema):
    count: int
    items: list[TokenRecordView] = Field(default_factory=list)


class TokenInspectParams(RpcSchema):
    token: str


class TokenInspectResult(RpcSchema):
    token_hash: str
    active: bool
    revoked: bool
    introspection: dict[str, Any] = Field(default_factory=dict)


class TokenExchangeParams(RpcSchema):
    subject_token: str
    requested_token_type: str | None = None
    audience: str | None = None
    resource: str | None = None
    actor_token: str | None = None
    extras: dict[str, Any] = Field(default_factory=dict)


class TokenExchangeResult(RpcSchema):
    status: str
    token: TokenRecordView | None = None


__all__ = [
    'TokenExchangeParams',
    'TokenExchangeResult',
    'TokenInspectParams',
    'TokenInspectResult',
    'TokenListParams',
    'TokenListResult',
    'TokenRecordView',
]
