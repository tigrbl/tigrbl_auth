"""Carrier-neutral process/runtime planning for identity deployments."""

from __future__ import annotations

from tigrbl_identity_runtime import RuntimePlan, build_runtime_plan
from tigrbl_identity_runtime.deployment import ResolvedDeployment, resolve_deployment


def _load_default_settings() -> object:
    from tigrbl_identity_runtime.settings import settings as default_settings

    return default_settings


def build_application_runtime_plan(
    settings_obj: object | None = None,
    *,
    deployment: ResolvedDeployment | None = None,
    runner: str = "uvicorn",
    environment: str = "development",
    app_factory: str = "unbound",
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
    jwks_refresh_seconds: int = 300,
    runner_options: dict[str, object] | None = None,
) -> RuntimePlan:
    resolved_deployment = deployment or resolve_deployment(settings_obj)
    return build_runtime_plan(
        settings_obj,
        deployment=resolved_deployment,
        runner=runner,
        environment=environment,
        app_factory=app_factory,
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
        jwks_refresh_seconds=jwks_refresh_seconds,
        runner_options=runner_options,
    )


__all__ = ["_load_default_settings", "build_application_runtime_plan"]
