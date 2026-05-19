"""Deployment-profile and certification-target introspection RPC methods."""

from __future__ import annotations

import json

from tigrbl_auth.api.rpc.registry import RpcMethodDefinition, RpcRequestContext
from tigrbl_auth.api.rpc.schemas.profile import (
    ProfileShowParams,
    ProfileShowResult,
    TargetListParams,
    TargetListResult,
    TargetShowParams,
    TargetShowResult,
)
from tigrbl_auth.api.rpc.methods._shared import deployment_summary, repo_root_from_context, read_yaml


def _resolved_deployment(context: RpcRequestContext):
    if context.deployment is not None:
        return context.deployment
    from tigrbl_auth.config.deployment import resolve_deployment

    return resolve_deployment(profile=context.profile)


def _load_state_json(repo_root, stem):
    path = repo_root / "docs" / "compliance" / f"{stem}.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


async def handle_profile_show(_params: ProfileShowParams, context: RpcRequestContext):
    deployment = _resolved_deployment(context)
    repo_root = repo_root_from_context(context)
    return ProfileShowResult(
        deployment=deployment_summary(deployment),
        current_state=_load_state_json(repo_root, "current_state_report"),
        certification_state=_load_state_json(repo_root, "certification_state_report"),
    )


async def handle_target_list(params: TargetListParams, context: RpcRequestContext):
    repo_root = repo_root_from_context(context)
    scope = read_yaml(repo_root / "compliance" / "targets" / "certification_scope.yaml") or {}
    targets = list(scope.get("targets", []))
    if params.scope_bucket:
        targets = [item for item in targets if str(item.get("scope_bucket")) == params.scope_bucket]
    return TargetListResult(count=len(targets), targets=targets)


async def handle_target_show(params: TargetShowParams, context: RpcRequestContext):
    repo_root = repo_root_from_context(context)
    scope = read_yaml(repo_root / "compliance" / "targets" / "certification_scope.yaml") or {}
    for item in scope.get("targets", []):
        if str(item.get("label")) == params.label:
            return TargetShowResult(target=item)
    return TargetShowResult(target=None)


METHODS = (
    RpcMethodDefinition(
        name="profile.show",
        summary="Show the effective deployment/profile posture.",
        description="Returns the effective deployment manifest together with current and certification state summaries.",
        params_model=ProfileShowParams,
        result_model=ProfileShowResult,
        handler=handle_profile_show,
        owner_module="tigrbl_auth/api/rpc/methods/profile.py",
        tags=("profile", "operator"),
    ),
    RpcMethodDefinition(
        name="target.list",
        summary="List certification-scope targets.",
        description="Returns the authoritative certification-scope target entries and their reality metadata.",
        params_model=TargetListParams,
        result_model=TargetListResult,
        handler=handle_target_list,
        owner_module="tigrbl_auth/api/rpc/methods/profile.py",
        tags=("profile", "certification"),
    ),
    RpcMethodDefinition(
        name="target.show",
        summary="Show a certification-scope target.",
        description="Returns a single certification-scope target entry by label.",
        params_model=TargetShowParams,
        result_model=TargetShowResult,
        handler=handle_target_show,
        owner_module="tigrbl_auth/api/rpc/methods/profile.py",
        tags=("profile", "certification"),
    ),
)
