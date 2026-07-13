from __future__ import annotations

from .assembly import (
    CONFIG_PRECEDENCE,
    ReadinessDiagnostic,
    ReadinessStatus,
    RuntimeProfile,
    provider_runtime_profile,
    readiness_diagnostic,
    resolve_config,
    resolve_feature_flags,
    testkit_provider_runtime_profile,
)
from .base import LazyASGIApplication, RunnerAdapter
from .registry import (
    get_runner_adapter,
    iter_runner_adapters,
    registered_runner_names,
    runner_registry_manifest,
)
from .standards import (
    STANDARD_OWNER_MODULES,
    RuntimeStandard,
    standard_version,
    standards_manifest,
)

__all__ = [
    "CONFIG_PRECEDENCE",
    "LazyASGIApplication",
    "ReadinessDiagnostic",
    "ReadinessStatus",
    "RunnerAdapter",
    "STANDARD_OWNER_MODULES",
    "RuntimeStandard",
    "RuntimeProfile",
    "RuntimePlan",
    "build_runtime_hash_matrix",
    "build_runtime_plan",
    "get_runner_adapter",
    "iter_runner_adapters",
    "provider_runtime_profile",
    "readiness_diagnostic",
    "registered_runner_names",
    "resolve_config",
    "resolve_feature_flags",
    "runner_registry_manifest",
    "standard_version",
    "standards_manifest",
    "testkit_provider_runtime_profile",
]


def __getattr__(name: str):
    if name in {"RuntimePlan", "build_runtime_hash_matrix", "build_runtime_plan"}:
        from . import plan

        return getattr(plan, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
