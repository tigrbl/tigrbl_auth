"""Schemas for audit lookup and export methods."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from .common import PaginationParams
from tigrbl_auth.api.rpc.registry import RpcSchema


class AuditEventRecord(RpcSchema):
    id: str
    tenant_id: str | None = None
    actor_user_id: str | None = None
    actor_client_id: str | None = None
    session_id: str | None = None
    event_type: str | None = None
    target_type: str | None = None
    target_id: str | None = None
    outcome: str | None = None
    request_id: str | None = None
    occurred_at: str | None = None
    details: dict[str, Any] = Field(default_factory=dict)


class AuditListParams(PaginationParams):
    event_type: str | None = None
    outcome: str | None = None


class AuditListResult(RpcSchema):
    count: int
    items: list[AuditEventRecord] = Field(default_factory=list)


class AuditExportParams(AuditListParams):
    export_format: str = Field(default="json")


class AuditExportResult(RpcSchema):
    export_format: str
    count: int
    content: str
    items: list[AuditEventRecord] = Field(default_factory=list)


__all__ = [
    "AuditEventRecord",
    "AuditExportParams",
    "AuditExportResult",
    "AuditListParams",
    "AuditListResult",
]
