"""Schemas for governance and control-plane RPC methods."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from .common import DeploymentSummary, EmptyParams, MethodSummary, OperationStatus
from tigrbl_auth.api.rpc.registry import RpcSchema


class RpcDiscoverResult(RpcSchema):
    deployment: DeploymentSummary
    method_count: int
    methods: list[MethodSummary] = Field(default_factory=list)


class FlowRecord(RpcSchema):
    name: str
    active: bool
    routes: list[str] = Field(default_factory=list)
    targets: list[str] = Field(default_factory=list)
    required_flags: list[str] = Field(default_factory=list)


class FlowListResult(RpcSchema):
    deployment: DeploymentSummary
    flows: list[FlowRecord] = Field(default_factory=list)


class DiscoveryShowResult(RpcSchema):
    deployment: DeploymentSummary
    metadata: dict[str, Any] = Field(default_factory=dict)


class ClaimsLintParams(EmptyParams):
    pass


class ClaimsLintResult(RpcSchema):
    passed: bool
    failures: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    report_path: str | None = None


class ClaimsShowParams(EmptyParams):
    pass


class ClaimsShowResult(RpcSchema):
    profile: str
    active_targets: list[str] = Field(default_factory=list)
    manifest: dict[str, Any] = Field(default_factory=dict)
    manifest_path: str | None = None


class GateRunParams(RpcSchema):
    gate: str


class GateRunResult(RpcSchema):
    passed: bool
    failures: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    details: list[dict[str, Any]] = Field(default_factory=list)


class EvidenceStatusParams(EmptyParams):
    pass


class EvidenceStatusResult(RpcSchema):
    passed: bool
    summary: dict[str, Any] = Field(default_factory=dict)
    failures: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class ReleaseBundleParams(RpcSchema):
    artifact: str = Field(default="all")
    bundle_dir: str | None = None


class ReleaseBundleResult(OperationStatus):
    bundle_path: str
    sha256: str | None = None


__all__ = [
    "ClaimsLintParams",
    "ClaimsLintResult",
    "ClaimsShowParams",
    "ClaimsShowResult",
    "DiscoveryShowResult",
    "EvidenceStatusParams",
    "EvidenceStatusResult",
    "FlowListResult",
    "FlowRecord",
    "GateRunParams",
    "GateRunResult",
    "ReleaseBundleParams",
    "ReleaseBundleResult",
    "RpcDiscoverResult",
]
