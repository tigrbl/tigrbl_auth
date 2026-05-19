from __future__ import annotations

from tigrbl_auth.api.app import build_app
from tigrbl_auth.config.deployment import ResolvedDeployment, resolve_deployment
from tigrbl_auth.runtime import LazyASGIApplication, RuntimePlan, build_runtime_plan

def resolve_gateway_deployment(settings_obj: object | None = None) -> ResolvedDeployment:
    return resolve_deployment(settings_obj, runtime_style="standalone")



def build_gateway(settings_obj: object | None = None):
    deployment = resolve_gateway_deployment(settings_obj)
    return build_app(settings_obj, deployment=deployment)



def build_gateway_runtime_plan(
    settings_obj: object | None = None,
    *,
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
    deployment = resolve_gateway_deployment(resolved_settings)
    return build_runtime_plan(
        resolved_settings,
        deployment=deployment,
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


app = LazyASGIApplication(build_gateway)

__all__ = ["app", "build_app", "build_gateway", "build_gateway_runtime_plan", "resolve_gateway_deployment"]
