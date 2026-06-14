"""Governance and control-plane RPC methods."""

from __future__ import annotations

import hashlib
import json

from tigrbl_identity_server.rpc.registry import RpcMethodDefinition, RpcRequestContext
from tigrbl_identity_contracts.rpc.common import EmptyParams
from tigrbl_identity_contracts.rpc.governance import (
    ClaimsLintParams,
    ClaimsLintResult,
    ClaimsShowParams,
    ClaimsShowResult,
    DiscoveryShowResult,
    EvidenceStatusParams,
    EvidenceStatusResult,
    FlowListResult,
    FlowRecord,
    GateRunParams,
    GateRunResult,
    ReleaseBundleParams,
    ReleaseBundleResult,
    RpcDiscoverResult,
)
from tigrbl_identity_admin.rpc._shared import deployment_summary, repo_root_from_context


def _resolved_deployment(context: RpcRequestContext):
    if context.deployment is not None:
        return context.deployment
    from tigrbl_identity_runtime.deployment import resolve_deployment

    return resolve_deployment(profile=context.profile)


async def handle_rpc_discover(_params, context: RpcRequestContext) -> RpcDiscoverResult:
    from tigrbl_identity_server.rpc import iter_active_rpc_methods

    deployment = _resolved_deployment(context)
    methods = [
        {
            "name": item.name,
            "summary": item.summary,
            "description": item.description,
            "owner_module": item.owner_module,
            "required_flags": list(item.required_flags),
            "tags": list(item.tags),
        }
        for item in iter_active_rpc_methods(deployment)
    ]
    return RpcDiscoverResult(
        deployment=deployment_summary(deployment),
        method_count=len(methods),
        methods=methods,
    )


async def handle_flow_list(_params, context: RpcRequestContext) -> FlowListResult:
    deployment = _resolved_deployment(context)
    from tigrbl_identity_runtime.deployment import PROTOCOL_SLICE_REGISTRY

    flows = []
    for name, meta in sorted(PROTOCOL_SLICE_REGISTRY.items()):
        flows.append(
            FlowRecord(
                name=name,
                active=name in getattr(deployment, "protocol_slices", ()),
                routes=list(meta.get("routes", ())),
                targets=list(meta.get("targets", ())),
                required_flags=list(meta.get("flags", ())),
            )
        )
    return FlowListResult(deployment=deployment_summary(deployment), flows=flows)


async def handle_discovery_show(_params, context: RpcRequestContext) -> DiscoveryShowResult:
    deployment = _resolved_deployment(context)
    metadata = {}
    try:
        from tigrbl_identity_oidc.standards.discovery import _build_openid_config
        metadata = _build_openid_config()
    except Exception:
        issuer = getattr(deployment, "issuer", "https://authn.example.com")
        metadata = {
            "issuer": issuer,
            "authorization_endpoint": f"{issuer}/authorize",
            "token_endpoint": f"{issuer}/token",
            "jwks_uri": f"{issuer}/.well-known/jwks.json",
            "end_session_endpoint": f"{issuer}/logout" if "/logout" in getattr(deployment, "active_routes", ()) else None,
        }
    return DiscoveryShowResult(
        deployment=deployment_summary(deployment),
        metadata={key: value for key, value in metadata.items() if value is not None},
    )


async def handle_claims_lint(_params: ClaimsLintParams, context: RpcRequestContext) -> ClaimsLintResult:
    repo_root = repo_root_from_context(context)
    from tigrbl_identity_cli.cli.claims import run_lint

    rc = run_lint(repo_root, strict=False, report_dir=repo_root / "docs" / "compliance")
    report_path = repo_root / "docs" / "compliance" / "claims_lint_report.json"
    payload = {}
    if report_path.exists():
        payload = json.loads(report_path.read_text(encoding="utf-8"))
    return ClaimsLintResult(
        passed=rc == 0 and bool(payload.get("passed", True)),
        failures=list(payload.get("failures", [])),
        warnings=list(payload.get("warnings", [])),
        report_path=str(report_path.relative_to(repo_root)) if report_path.exists() else None,
    )


async def handle_claims_show(_params: ClaimsShowParams, context: RpcRequestContext) -> ClaimsShowResult:
    repo_root = repo_root_from_context(context)
    deployment = _resolved_deployment(context)
    from tigrbl_identity_cli.cli.artifacts import write_effective_claims_manifest
    import yaml

    manifest_path = write_effective_claims_manifest(repo_root, deployment, profile_label=deployment.profile)
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    return ClaimsShowResult(
        profile=deployment.profile,
        active_targets=list(getattr(deployment, "active_targets", ()) or ()),
        manifest=manifest,
        manifest_path=str(manifest_path.relative_to(repo_root)),
    )


async def handle_gate_run(params: GateRunParams, context: RpcRequestContext) -> GateRunResult:
    repo_root = repo_root_from_context(context)
    from tigrbl_identity_cli.cli.reports import run_release_gates

    payload = run_release_gates(repo_root, gate_name=params.gate, strict=False)
    return GateRunResult(
        passed=bool(payload.get("passed", False)),
        failures=list(payload.get("failures", [])),
        warnings=list(payload.get("warnings", [])),
        details=list(payload.get("details", [])),
    )


async def handle_evidence_status(_params: EvidenceStatusParams, context: RpcRequestContext) -> EvidenceStatusResult:
    repo_root = repo_root_from_context(context)
    from tigrbl_identity_cli.cli.reports import summarize_evidence_status

    payload = summarize_evidence_status(repo_root)
    return EvidenceStatusResult(
        passed=bool(payload.get("passed", False)),
        summary=dict(payload.get("summary", {})),
        failures=list(payload.get("failures", [])),
        warnings=list(payload.get("warnings", [])),
    )


async def handle_release_bundle(params: ReleaseBundleParams, context: RpcRequestContext) -> ReleaseBundleResult:
    repo_root = repo_root_from_context(context)
    deployment = _resolved_deployment(context)
    from pathlib import Path
    from tigrbl_identity_cli.cli.reports import build_release_bundle

    bundle_path = build_release_bundle(
        repo_root,
        deployment,
        bundle_dir=Path(params.bundle_dir).resolve() if params.bundle_dir else None,
        artifact=params.artifact,
    )
    sha256 = hashlib.sha256(bundle_path.read_bytes()).hexdigest() if bundle_path.exists() and bundle_path.is_file() else None
    return ReleaseBundleResult(
        status="ok",
        message="release bundle built",
        bundle_path=str(bundle_path),
        sha256=sha256,
    )


METHODS = (
    RpcMethodDefinition(
        name="rpc.discover",
        summary="Return the active implementation-backed RPC method catalog.",
        description="Discovers the operator/admin RPC methods derived from executable registration.",
        params_model=EmptyParams,
        result_model=RpcDiscoverResult,
        handler=handle_rpc_discover,
        owner_module="tigrbl_auth/api/rpc/methods/governance.py",
        tags=("discovery", "rpc"),
    ),
    RpcMethodDefinition(
        name="flow.list",
        summary="List effective protocol flow slices for the current deployment.",
        description="Summarizes active protocol slices, routes, required flags, and mapped targets.",
        params_model=EmptyParams,
        result_model=FlowListResult,
        handler=handle_flow_list,
        owner_module="tigrbl_auth/api/rpc/methods/governance.py",
        tags=("deployment", "flows"),
    ),
    RpcMethodDefinition(
        name="discovery.show",
        summary="Show effective OIDC discovery metadata for the deployment.",
        description="Returns the effective discovery document as currently configured.",
        params_model=EmptyParams,
        result_model=DiscoveryShowResult,
        handler=handle_discovery_show,
        owner_module="tigrbl_auth/api/rpc/methods/governance.py",
        tags=("discovery", "oidc"),
    ),
    RpcMethodDefinition(
        name="claims.lint",
        summary="Run claims lint against the governance plane.",
        description="Executes the claims lint pipeline and returns the summarized result.",
        params_model=ClaimsLintParams,
        result_model=ClaimsLintResult,
        handler=handle_claims_lint,
        owner_module="tigrbl_auth/api/rpc/methods/governance.py",
        tags=("governance", "claims"),
    ),
    RpcMethodDefinition(
        name="claims.show",
        summary="Return effective claims for the active deployment profile.",
        description="Builds and returns the effective target-claims manifest.",
        params_model=ClaimsShowParams,
        result_model=ClaimsShowResult,
        handler=handle_claims_show,
        owner_module="tigrbl_auth/api/rpc/methods/governance.py",
        tags=("governance", "claims"),
    ),
    RpcMethodDefinition(
        name="gate.run",
        summary="Run a named release gate.",
        description="Executes a configured release gate and returns pass/fail status with details.",
        params_model=GateRunParams,
        result_model=GateRunResult,
        handler=handle_gate_run,
        owner_module="tigrbl_auth/api/rpc/methods/governance.py",
        tags=("governance", "release"),
    ),
    RpcMethodDefinition(
        name="evidence.status",
        summary="Summarize evidence-plane status.",
        description="Returns the evidence readiness summary, failures, and warnings.",
        params_model=EvidenceStatusParams,
        result_model=EvidenceStatusResult,
        handler=handle_evidence_status,
        owner_module="tigrbl_auth/api/rpc/methods/governance.py",
        tags=("governance", "evidence"),
    ),
    RpcMethodDefinition(
        name="release.bundle",
        summary="Build a release bundle.",
        description="Builds the current release bundle and returns its path and digest.",
        params_model=ReleaseBundleParams,
        result_model=ReleaseBundleResult,
        handler=handle_release_bundle,
        owner_module="tigrbl_auth/api/rpc/methods/governance.py",
        tags=("governance", "release"),
    ),
)

# Discovery RPC resolves through the shared discovery service layer.
from tigrbl_identity_oidc.discovery_service import show_discovery as _svc_show_discovery


async def handle_discovery_show(_params, context: RpcRequestContext) -> DiscoveryShowResult:
    deployment = _resolved_deployment(context)
    payload = _svc_show_discovery(repo_root_from_context(context), profile=getattr(deployment, 'profile', None))
    documents = payload.get('documents', {})
    metadata = documents.get('openid-configuration.json') or documents.get('oauth-authorization-server.json') or {}
    return DiscoveryShowResult(
        deployment=deployment_summary(deployment),
        metadata={key: value for key, value in metadata.items() if value is not None},
    )


METHODS = tuple(
    RpcMethodDefinition(
        name=item.name,
        summary=item.summary,
        description=item.description,
        params_model=item.params_model,
        result_model=item.result_model,
        handler=handle_discovery_show if item.name == 'discovery.show' else item.handler,
        owner_module=item.owner_module,
        tags=item.tags,
        required_flags=item.required_flags,
    )
    for item in METHODS
)
