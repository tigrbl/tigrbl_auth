from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Mapping


class ReadinessStatus(str, Enum):
    READY = "ready"
    NOT_READY = "not_ready"


@dataclass(frozen=True, slots=True)
class RuntimeProfile:
    name: str
    server_profile: str
    runner: str = "uvicorn"
    feature_flags: Mapping[str, bool] = field(default_factory=dict)
    config: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.runner not in {"uvicorn", "hypercorn", "tigrcorn", "gunicorn"}:
            raise ValueError("unsupported runner")
        object.__setattr__(self, "feature_flags", dict(self.feature_flags))
        object.__setattr__(self, "config", dict(self.config))


@dataclass(frozen=True, slots=True)
class ReadinessDiagnostic:
    status: ReadinessStatus
    profile: str
    checks: Mapping[str, bool]
    error: str | None = None

    @property
    def ready(self) -> bool:
        return self.status == ReadinessStatus.READY


CONFIG_PRECEDENCE = ("defaults", "profile", "environment", "explicit")


def resolve_config(
    *,
    defaults: Mapping[str, str] | None = None,
    profile: Mapping[str, str] | None = None,
    environment: Mapping[str, str] | None = None,
    explicit: Mapping[str, str] | None = None,
) -> dict[str, str]:
    resolved: dict[str, str] = {}
    for layer in (defaults or {}, profile or {}, environment or {}, explicit or {}):
        resolved.update({key: value for key, value in layer.items() if value is not None})
    return resolved


def resolve_feature_flags(
    *,
    defaults: Mapping[str, bool] | None = None,
    profile: Mapping[str, bool] | None = None,
    explicit: Mapping[str, bool] | None = None,
) -> dict[str, bool]:
    flags: dict[str, bool] = {}
    for layer in (defaults or {}, profile or {}, explicit or {}):
        flags.update({key: bool(value) for key, value in layer.items()})
    return flags


def provider_runtime_profile() -> RuntimeProfile:
    return RuntimeProfile(
        name="provider-runtime",
        server_profile="provider",
        runner="uvicorn",
        feature_flags={
            "surface_public_enabled": True,
            "surface_admin_enabled": True,
            "surface_rpc_enabled": True,
            "surface_diagnostics_enabled": True,
        },
        config={"mode": "provider"},
    )


def testkit_provider_runtime_profile() -> RuntimeProfile:
    base = provider_runtime_profile()
    return RuntimeProfile(
        name="testkit-provider-runtime",
        server_profile=base.server_profile,
        runner="uvicorn",
        feature_flags={**base.feature_flags, "seed_test_tenant": True, "enable_test_clients": True},
        config={**base.config, "mode": "testkit", "tenant_id": "test"},
    )


def readiness_diagnostic(profile: RuntimeProfile, checks: Mapping[str, bool], error: str | None = None) -> ReadinessDiagnostic:
    ok = all(checks.values()) and error is None
    return ReadinessDiagnostic(
        status=ReadinessStatus.READY if ok else ReadinessStatus.NOT_READY,
        profile=profile.name,
        checks=dict(checks),
        error=error,
    )


__all__ = [
    "CONFIG_PRECEDENCE",
    "ReadinessDiagnostic",
    "ReadinessStatus",
    "RuntimeProfile",
    "provider_runtime_profile",
    "readiness_diagnostic",
    "resolve_config",
    "resolve_feature_flags",
    "testkit_provider_runtime_profile",
]
