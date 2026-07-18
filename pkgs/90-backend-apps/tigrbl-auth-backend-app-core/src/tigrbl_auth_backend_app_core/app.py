from __future__ import annotations

from dataclasses import replace
from importlib.metadata import (
    PackageNotFoundError,
    version as installed_package_version,
)
from pathlib import Path
from typing import TYPE_CHECKING

from tigrbl_identity_runtime.deployment import ResolvedDeployment, resolve_deployment
from tigrbl_identity_operator.repo_truth import (
    package_version as repository_package_version,
)
from tigrbl_identity_runtime import LazyASGIApplication
from tigrbl_identity_server.composition.app import (
    _load_default_settings,
    build_application_runtime_plan as _build_application_runtime_plan,
)

if TYPE_CHECKING:
    from tigrbl import TigrblApp
    from tigrbl_identity_server.composition.lifecycle import AssemblyFactory


def _runtime_package_version() -> str:
    try:
        return installed_package_version("tigrbl-auth-backend-app-core")
    except PackageNotFoundError:
        return repository_package_version(Path(__file__).resolve().parents[2])


def _path_has_prefix(path: str, prefix: str) -> bool:
    return path == prefix or path.startswith(f"{prefix}/")


def _hide_disabled_control_plane_docs(
    app: object,
    deployment: ResolvedDeployment,
    *,
    diagnostics_prefix: str,
) -> None:
    routes = getattr(app, "_routes", None)
    if not isinstance(routes, list):
        return

    hidden = []
    for route in routes:
        path = str(getattr(route, "path_template", None) or getattr(route, "path", ""))
        hide = not deployment.flag_enabled(
            "surface_diagnostics_enabled"
        ) and _path_has_prefix(path, diagnostics_prefix)
        if hide and hasattr(route, "include_in_schema"):
            hidden.append(replace(route, include_in_schema=False))
        else:
            hidden.append(route)
    routes[:] = hidden


def build_app(
    settings_obj: object | None = None,
    *,
    deployment: ResolvedDeployment | None = None,
    runtime_assembly_factory: AssemblyFactory | None = None,
) -> "TigrblApp":
    resolved_settings = (
        settings_obj if settings_obj is not None else _load_default_settings()
    )
    resolved_deployment = deployment or resolve_deployment(resolved_settings)
    if runtime_assembly_factory is None:
        from tigrbl_identity_server.composition.runtime_assembly import (
            build_server_runtime_assembly_async,
        )

        async def default_runtime_assembly_factory():
            return await build_server_runtime_assembly_async(resolved_settings)

        runtime_assembly_factory = default_runtime_assembly_factory

    from tigrbl_identity_contracts.protocol_configuration import (
        ProtocolSettingsOverlay,
        bind_protocol_settings,
    )

    protocol_settings = ProtocolSettingsOverlay(
        resolved_settings, _load_default_settings()
    )
    bind_protocol_settings(protocol_settings)

    from tigrbl import TigrblApp

    from tigrbl_identity_server.composition.lifecycle import register_lifecycle
    from tigrbl_auth_backend_app_core.surfaces import (
        admin_resource_path_prefixes,
        attach_runtime_surfaces,
    )
    from tigrbl_auth_router_admin_gate import AdminGate
    from tigrbl_identity_storage_runtime.engine import dsn

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
    surface_router = attach_runtime_surfaces(
        app,
        resolved_settings,
        deployment=resolved_deployment,
        diagnostics_prefix="/system",
    )
    _hide_disabled_control_plane_docs(
        app,
        resolved_deployment,
        diagnostics_prefix="/system",
    )
    register_lifecycle(
        app,
        assembly_factory=runtime_assembly_factory,
        surface_initializer=surface_router.initialize,
    )
    return AdminGate(
        app,
        deployment=resolved_deployment,
        settings_obj=resolved_settings,
        admin_path_prefixes=admin_resource_path_prefixes(resolved_deployment),
        diagnostics_prefix="/system",
    )


def build_application_runtime_plan(*args: object, **kwargs: object):
    kwargs.setdefault(
        "app_factory",
        "tigrbl_auth_backend_app_core.app.build_app",
    )
    return _build_application_runtime_plan(*args, **kwargs)


app = LazyASGIApplication(build_app)

__all__ = ["app", "build_app", "build_application_runtime_plan"]
