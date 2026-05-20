from __future__ import annotations

from .base import LazyASGIApplication, RunnerAdapter
from .registry import get_runner_adapter, iter_runner_adapters, registered_runner_names, runner_registry_manifest

__all__ = [
    "LazyASGIApplication",
    "RunnerAdapter",
    "RuntimePlan",
    "build_runtime_hash_matrix",
    "build_runtime_plan",
    "get_runner_adapter",
    "iter_runner_adapters",
    "registered_runner_names",
    "runner_registry_manifest",
]


def __getattr__(name: str):
    if name in {"RuntimePlan", "build_runtime_hash_matrix", "build_runtime_plan"}:
        from . import plan

        return getattr(plan, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
