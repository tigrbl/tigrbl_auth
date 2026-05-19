"""Schemas for session admin RPC methods."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from .common import PaginationParams
from tigrbl_auth.api.rpc.registry import RpcSchema


class SessionRecord(RpcSchema):
    id: str
    user_id: str | None = None
    tenant_id: str | None = None
    username: str | None = None
    client_id: str | None = None
    auth_time: str | None = None
    session_state: str | None = None
    expires_at: str | None = None
    last_seen_at: str | None = None
    ended_at: str | None = None
    logout_reason: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class SessionListParams(PaginationParams):
    active_only: bool = False
    user_id: str | None = None
    client_id: str | None = None
    tenant_id: str | None = None


class SessionListResult(RpcSchema):
    count: int
    items: list[SessionRecord] = Field(default_factory=list)


class SessionShowParams(RpcSchema):
    session_id: str


class SessionShowResult(RpcSchema):
    session: SessionRecord | None = None
    latest_logout: dict[str, Any] | None = None


class SessionTerminateParams(RpcSchema):
    session_id: str
    initiated_by: str = "operator"
    reason: str = "administrative_logout"
    frontchannel_required: bool = False
    backchannel_required: bool = False
    metadata: dict[str, Any] = Field(default_factory=dict)


class SessionTerminateResult(RpcSchema):
    session: SessionRecord | None = None
    logout_state: dict[str, Any] | None = None


__all__ = [
    "SessionListParams",
    "SessionListResult",
    "SessionRecord",
    "SessionShowParams",
    "SessionShowResult",
    "SessionTerminateParams",
    "SessionTerminateResult",
]
