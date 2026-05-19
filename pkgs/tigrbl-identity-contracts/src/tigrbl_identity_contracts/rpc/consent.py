"""Schemas for consent inspection and revocation."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from .common import PaginationParams
from tigrbl_auth.api.rpc.registry import RpcSchema


class ConsentRecord(RpcSchema):
    id: str
    user_id: str | None = None
    tenant_id: str | None = None
    client_id: str | None = None
    scope: str | None = None
    state: str | None = None
    granted_at: str | None = None
    expires_at: str | None = None
    revoked_at: str | None = None
    claims: dict[str, Any] = Field(default_factory=dict)


class ConsentListParams(PaginationParams):
    user_id: str | None = None
    client_id: str | None = None
    state: str | None = None


class ConsentListResult(RpcSchema):
    count: int
    items: list[ConsentRecord] = Field(default_factory=list)


class ConsentShowParams(RpcSchema):
    consent_id: str


class ConsentShowResult(RpcSchema):
    consent: ConsentRecord | None = None


class ConsentRevokeParams(RpcSchema):
    consent_id: str


class ConsentRevokeResult(RpcSchema):
    consent: ConsentRecord | None = None


__all__ = [
    "ConsentListParams",
    "ConsentListResult",
    "ConsentRecord",
    "ConsentRevokeParams",
    "ConsentRevokeResult",
    "ConsentShowParams",
    "ConsentShowResult",
]
