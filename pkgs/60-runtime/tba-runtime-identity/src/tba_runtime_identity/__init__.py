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
from .engine import ENGINE, bootstrap_runtime_engine, dsn, get_db
from .capability_registry import CapabilityFactory, CapabilityRegistry
from .capability_assembly import (
    ProtocolCapabilityBindingError,
    RuntimeCapabilityAssembly,
    build_runtime_capability_assembly,
    validate_protocol_capabilities,
)
from .composition.webauthn import WebAuthnComposition, build_webauthn_composition
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
    "CapabilityRegistry",
    "CapabilityFactory",
    "LazyASGIApplication",
    "ProtocolCapabilityBindingError",
    "ReadinessDiagnostic",
    "ReadinessStatus",
    "RunnerAdapter",
    "STANDARD_OWNER_MODULES",
    "RuntimeStandard",
    "RuntimeProfile",
    "RuntimeCapabilityAssembly",
    "RuntimePlan",
    "build_runtime_hash_matrix",
    "build_runtime_capability_assembly",
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
    "validate_protocol_capabilities",
    "WebAuthnComposition",
    "build_webauthn_composition",
    "ENGINE",
    "bootstrap_runtime_engine",
    "dsn",
    "get_db",
]


def __getattr__(name: str):
    if name in {"RuntimePlan", "build_runtime_hash_matrix", "build_runtime_plan"}:
        from . import plan

        return getattr(plan, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
