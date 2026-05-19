"""Schemas for key and JWKS operator methods."""

from __future__ import annotations

from typing import Any

from .common import EmptyParams
from pydantic import Field
from tigrbl_auth.api.rpc.registry import RpcSchema


class KeyRecord(RpcSchema):
    id: str
    kind: str
    kid: str | None = None
    label: str | None = None
    service_id: str | None = None
    digest: str | None = None
    created_at: str | None = None
    valid_from: str | None = None
    valid_to: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class KeysListParams(EmptyParams):
    pass


class KeysListResult(RpcSchema):
    key_count: int
    rotation_event_count: int
    keys: list[KeyRecord] = Field(default_factory=list)
    rotation_events: list[dict[str, Any]] = Field(default_factory=list)


class JwksShowParams(EmptyParams):
    pass


class JwksShowResult(RpcSchema):
    jwks: dict[str, Any] = Field(default_factory=dict)


class KeysRotateParams(RpcSchema):
    reason: str = "operator_rotation"


class KeysRotateResult(RpcSchema):
    status: str = "rotated"
    new_kid: str
    rotation_event: dict[str, Any] | None = None


__all__ = [
    "JwksShowParams",
    "JwksShowResult",
    "KeyRecord",
    "KeysListParams",
    "KeysListResult",
    "KeysRotateParams",
    "KeysRotateResult",
]
