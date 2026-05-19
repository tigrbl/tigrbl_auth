"""Schemas for deployment/profile/target introspection."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from .common import DeploymentSummary, EmptyParams
from tigrbl_auth.api.rpc.registry import RpcSchema


class ProfileShowParams(EmptyParams):
    pass


class ProfileShowResult(RpcSchema):
    deployment: DeploymentSummary
    current_state: dict[str, Any] = Field(default_factory=dict)
    certification_state: dict[str, Any] = Field(default_factory=dict)


class TargetListParams(EmptyParams):
    scope_bucket: str | None = None


class TargetSummary(RpcSchema):
    label: str
    id: str | None = None
    scope_bucket: str
    owner_modules: list[str] = Field(default_factory=list)
    endpoint_surface: dict[str, Any] = Field(default_factory=dict)
    test_classes: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    profile_reality: dict[str, Any] = Field(default_factory=dict)
    discrepancies: list[str] = Field(default_factory=list)


class TargetListResult(RpcSchema):
    count: int
    targets: list[TargetSummary] = Field(default_factory=list)


class TargetShowParams(RpcSchema):
    label: str


class TargetShowResult(RpcSchema):
    target: TargetSummary | None = None


__all__ = [
    "ProfileShowParams",
    "ProfileShowResult",
    "TargetListParams",
    "TargetListResult",
    "TargetShowParams",
    "TargetShowResult",
    "TargetSummary",
]
