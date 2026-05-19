"""Shared RPC schema primitives."""

from __future__ import annotations

from typing import Any

from pydantic import ConfigDict, Field

from tigrbl_auth.api.rpc.registry import EmptyParams, RpcSchema


class PaginationParams(RpcSchema):
    limit: int = Field(default=50, ge=1, le=200)
    offset: int = Field(default=0, ge=0)


class OperationStatus(RpcSchema):
    status: str = "ok"
    message: str | None = None


class MethodSummary(RpcSchema):
    name: str
    summary: str
    description: str
    owner_module: str
    required_flags: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)


class DeploymentSummary(RpcSchema):
    profile: str
    plugin_mode: str
    runtime_style: str
    surface_sets: list[str] = Field(default_factory=list)
    protocol_slices: list[str] = Field(default_factory=list)
    active_routes: list[str] = Field(default_factory=list)
    active_targets: list[str] = Field(default_factory=list)
    active_openrpc_methods: list[str] = Field(default_factory=list)


class KeyValueDocument(RpcSchema):
    model_config = ConfigDict(extra="allow")
    data: dict[str, Any] = Field(default_factory=dict)


__all__ = [
    "DeploymentSummary",
    "EmptyParams",
    "KeyValueDocument",
    "MethodSummary",
    "OperationStatus",
    "PaginationParams",
]
