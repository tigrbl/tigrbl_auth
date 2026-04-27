from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version as installed_package_version
from pathlib import Path
from typing import TYPE_CHECKING

from tigrbl_auth.config.deployment import ResolvedDeployment, resolve_deployment
from tigrbl_auth.repo_truth import package_version as repository_package_version
from tigrbl_auth.runtime import LazyASGIApplication, RuntimePlan, build_runtime_plan

if TYPE_CHECKING:
    from tigrbl import TigrblApp


def _load_default_settings() -> object:
    from tigrbl_auth.config.settings import settings as default_settings

    return default_settings


def _runtime_package_version() -> str:
    try:
        return installed_package_version("tigrbl_auth")
    except PackageNotFoundError:
        return repository_package_version(Path(__file__).resolve().parents[2])


def build_app(
    settings_obj: object | None = None,
    *,
    deployment: ResolvedDeployment | None = None,
) -> "TigrblApp":
    resolved_settings = settings_obj if settings_obj is not None else _load_default_settings()
    resolved_deployment = deployment or resolve_deployment(resolved_settings)

    from tigrbl import TigrblApp

    from tigrbl_auth.api.lifecycle import register_lifecycle
    from tigrbl_auth.api.surfaces import admin_resource_path_prefixes, attach_runtime_surfaces
    from tigrbl_auth.security.admin_gate import AdminGate
    from tigrbl_auth.security.openapi import install_tigrbl_openapi_security_compat
    from tigrbl_auth.tables.engine import dsn

    install_tigrbl_openapi_security_compat()
    app = TigrblApp(
        title="tigrbl_auth",
        version=_runtime_package_version(),
        openapi_url="/openapi.json",
        docs_url="/docs",
        engine=dsn,
    )
    state = getattr(app, "state", None)
    if state is not None:
        state.tigrbl_auth_deployment = resolved_deployment
        state.tigrbl_auth_settings = resolved_settings
    attach_runtime_surfaces(
        app,
        resolved_settings,
        deployment=resolved_deployment,
        rpc_prefix="/rpc",
        diagnostics_prefix="/system",
    )
    register_lifecycle(app)
    return AdminGate(
        app,
        deployment=resolved_deployment,
        settings_obj=resolved_settings,
        admin_path_prefixes=admin_resource_path_prefixes(),
        rpc_prefix="/rpc",
        diagnostics_prefix="/system",
    )



def build_application_runtime_plan(
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
    jwks_refresh_seconds: int = 300,
    runner_options: dict[str, object] | None = None,
) -> RuntimePlan:
    resolved_settings = settings_obj
    resolved_deployment = deployment or resolve_deployment(resolved_settings)
    return build_runtime_plan(
        resolved_settings,
        deployment=resolved_deployment,
        runner=runner,
        environment=environment,
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


app = LazyASGIApplication(build_app)

__all__ = ["app", "build_app", "build_application_runtime_plan"]
