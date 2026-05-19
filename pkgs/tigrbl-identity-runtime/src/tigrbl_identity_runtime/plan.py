from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field, replace
from typing import Any

from tigrbl_auth.config.deployment import ResolvedDeployment, resolve_deployment

from .types import RunnerCapability, RunnerFlagMetadata, RuntimeDiagnostic


def _stable_hash(payload: Any) -> str:
    rendered = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(rendered.encode("utf-8")).hexdigest()


def _deployment_manifest(deployment: Any) -> dict[str, Any]:
    to_manifest = getattr(deployment, "to_manifest", None)
    if callable(to_manifest):
        payload = to_manifest()
        if isinstance(payload, dict):
            return payload
    return {
        "profile": str(getattr(deployment, "profile", "baseline")),
        "runtime_style": str(getattr(deployment, "runtime_style", "portable")),
        "plugin_mode": str(getattr(deployment, "plugin_mode", "self-contained")),
        "surfaces": dict(getattr(deployment, "surfaces", {}) or {}),
        "flags": dict(getattr(deployment, "flags", {}) or {}),
    }


@dataclass(slots=True, frozen=True)
class RuntimePlan:
    profile: str
    runtime_style: str
    plugin_mode: str
    runner: str
    environment: str
    app_factory: str
    deployment: ResolvedDeployment
    host: str = "127.0.0.1"
    port: int = 8000
    workers: int = 1
    uds: str | None = None
    log_level: str = "INFO"
    access_log: bool = True
    lifespan: str = "auto"
    graceful_timeout: int = 30
    pid_file: str | None = None
    proxy_headers: bool = False
    require_tls: bool = True
    enable_mtls: bool = False
    cookies: bool = True
    health: bool = True
    metrics: bool = True
    public: bool = True
    admin: bool = True
    rpc: bool = True
    diagnostics: bool = True
    jwks_refresh_seconds: int = 300
    runner_options: dict[str, Any] = field(default_factory=dict)
    runner_capabilities: tuple[RunnerCapability, ...] = ()
    runner_flag_metadata: tuple[RunnerFlagMetadata, ...] = ()
    diagnostics_report: tuple[RuntimeDiagnostic, ...] = ()

    def application_manifest(self) -> dict[str, Any]:
        return {
            "profile": self.profile,
            "runtime_style": self.runtime_style,
            "plugin_mode": self.plugin_mode,
            "environment": self.environment,
            "app_factory": self.app_factory,
            "deployment": _deployment_manifest(self.deployment),
            "surface_toggles": {
                "public": self.public,
                "admin": self.admin,
                "rpc": self.rpc,
                "diagnostics": self.diagnostics,
            },
            "security_toggles": {
                "require_tls": self.require_tls,
                "enable_mtls": self.enable_mtls,
                "cookies": self.cookies,
            },
            "observability": {
                "health": self.health,
                "metrics": self.metrics,
                "log_level": self.log_level,
                "jwks_refresh_seconds": self.jwks_refresh_seconds,
            },
        }

    def runtime_manifest(self) -> dict[str, Any]:
        return {
            "runner": self.runner,
            "bind": {
                "host": self.host,
                "port": self.port,
                "workers": self.workers,
                "uds": self.uds,
            },
            "logging": {
                "log_level": self.log_level,
                "access_log": self.access_log,
            },
            "lifecycle": {
                "lifespan": self.lifespan,
                "graceful_timeout": self.graceful_timeout,
                "pid_file": self.pid_file,
            },
            "proxy_headers": self.proxy_headers,
            "runner_options": dict(self.runner_options),
            "capabilities": [item.to_manifest() for item in self.runner_capabilities],
            "flag_metadata": [item.to_manifest() for item in self.runner_flag_metadata],
            "diagnostics": [item.to_manifest() for item in self.diagnostics_report],
        }

    @property
    def application_hash(self) -> str:
        return _stable_hash(self.application_manifest())

    @property
    def runtime_hash(self) -> str:
        return _stable_hash(
            {
                "application_hash": self.application_hash,
                "runtime": self.runtime_manifest(),
            }
        )

    def to_manifest(self) -> dict[str, Any]:
        return {
            **self.application_manifest(),
            **self.runtime_manifest(),
            "application_hash": self.application_hash,
            "runtime_hash": self.runtime_hash,
        }


def build_runtime_plan(
    settings_obj: object | None = None,
    *,
    deployment: ResolvedDeployment | None = None,
    runner: str = "uvicorn",
    environment: str = "development",
    host: str = "127.0.0.1",
    port: int = 8000,
    workers: int = 1,
    uds: str | None = None,
    log_level: str = "INFO",
    access_log: bool = True,
    lifespan: str = "auto",
    graceful_timeout: int = 30,
    pid_file: str | None = None,
    proxy_headers: bool = False,
    require_tls: bool = True,
    enable_mtls: bool = False,
    cookies: bool = True,
    health: bool = True,
    metrics: bool = True,
    public: bool | None = None,
    admin: bool | None = None,
    rpc: bool | None = None,
    diagnostics: bool | None = None,
    jwks_refresh_seconds: int = 300,
    runner_options: dict[str, Any] | None = None,
) -> RuntimePlan:
    from .registry import get_runner_adapter

    resolved_settings = settings_obj
    resolved_deployment = deployment or resolve_deployment(resolved_settings)
    adapter = get_runner_adapter(runner)
    deployment_profile = str(getattr(resolved_deployment, "profile", "baseline"))
    deployment_runtime_style = str(getattr(resolved_deployment, "runtime_style", "portable"))
    deployment_plugin_mode = str(getattr(resolved_deployment, "plugin_mode", "self-contained"))
    deployment_surfaces = getattr(resolved_deployment, "surfaces", {}) or {}
    plan = RuntimePlan(
        profile=deployment_profile,
        runtime_style=deployment_runtime_style,
        plugin_mode=deployment_plugin_mode,
        runner=adapter.name,
        environment=environment,
        app_factory="tigrbl_auth.api.app.build_app",
        deployment=resolved_deployment,
        host=host,
        port=port,
        workers=workers,
        uds=uds,
        log_level=log_level,
        access_log=access_log,
        lifespan=lifespan,
        graceful_timeout=graceful_timeout,
        pid_file=pid_file,
        proxy_headers=proxy_headers,
        require_tls=require_tls,
        enable_mtls=enable_mtls,
        cookies=cookies,
        health=health,
        metrics=metrics,
        public=bool(deployment_surfaces.get("surface_public_enabled", False)) if public is None else bool(public),
        admin=bool(deployment_surfaces.get("surface_admin_enabled", False)) if admin is None else bool(admin),
        rpc=bool(deployment_surfaces.get("surface_rpc_enabled", False)) if rpc is None else bool(rpc),
        diagnostics=bool(deployment_surfaces.get("surface_diagnostics_enabled", False)) if diagnostics is None else bool(diagnostics),
        jwks_refresh_seconds=jwks_refresh_seconds,
        runner_options=dict(runner_options or {}),
        runner_capabilities=tuple(adapter.capabilities),
        runner_flag_metadata=tuple(adapter.flag_metadata),
        diagnostics_report=(),
    )
    return replace(plan, diagnostics_report=adapter.validate(plan))


def build_runtime_hash_matrix(
    settings_obj: object | None = None,
    *,
    deployment: ResolvedDeployment | None = None,
    environment: str = "development",
    host: str = "127.0.0.1",
    port: int = 8000,
    workers: int = 1,
    access_log: bool = True,
    lifespan: str = "auto",
    graceful_timeout: int = 30,
) -> dict[str, dict[str, str]]:
    from .registry import registered_runner_names

    matrix: dict[str, dict[str, str]] = {}
    for runner in registered_runner_names():
        plan = build_runtime_plan(
            settings_obj,
            deployment=deployment,
            runner=runner,
            environment=environment,
            host=host,
            port=port,
            workers=workers,
            access_log=access_log,
            lifespan=lifespan,
            graceful_timeout=graceful_timeout,
        )
        matrix[runner] = {
            "application_hash": plan.application_hash,
            "runtime_hash": plan.runtime_hash,
        }
    return matrix


__all__ = ["RuntimePlan", "build_runtime_hash_matrix", "build_runtime_plan"]
