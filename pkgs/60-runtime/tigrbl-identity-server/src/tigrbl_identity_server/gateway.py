"""Standalone gateway runtime planning without HTTP carrier ownership."""

from __future__ import annotations

from tigrbl_identity_runtime import RuntimePlan, build_runtime_plan
from tigrbl_identity_runtime.deployment import ResolvedDeployment, resolve_deployment


def resolve_gateway_deployment(
    settings_obj: object | None = None,
) -> ResolvedDeployment:
    return resolve_deployment(settings_obj, runtime_style="standalone")


def build_gateway_runtime_plan(
    settings_obj: object | None = None,
    **runtime_options: object,
) -> RuntimePlan:
    deployment = resolve_gateway_deployment(settings_obj)
    return build_runtime_plan(settings_obj, deployment=deployment, **runtime_options)


__all__ = ["build_gateway_runtime_plan", "resolve_gateway_deployment"]
