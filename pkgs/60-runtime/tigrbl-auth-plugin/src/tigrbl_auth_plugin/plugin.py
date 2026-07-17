from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from tigrbl_identity_runtime.deployment import ResolvedDeployment, resolve_deployment

if TYPE_CHECKING:
    from tigrbl import TigrblApp


SurfaceAttacher = Callable[..., Any]


@dataclass(slots=True, kw_only=True)
class TigrblAuthPlugin:
    """Bind identity runtime lifecycle around an injected HTTP surface attacher."""

    surface_attacher: SurfaceAttacher
    diagnostics_prefix: str = "/system"
    settings: object | None = None

    def resolve_plugin_deployment(
        self, settings: object | None = None
    ) -> ResolvedDeployment:
        resolved_settings = settings if settings is not None else self.settings
        return resolve_deployment(resolved_settings, runtime_style="plugin")

    def install(self, app: "TigrblApp", settings: object | None = None) -> "TigrblApp":
        resolved_settings = settings if settings is not None else self.settings
        deployment = self.resolve_plugin_deployment(resolved_settings)

        from tigrbl_identity_server.api.lifecycle import register_lifecycle

        state = getattr(app, "state", None)
        if state is not None:
            state.tigrbl_auth_deployment = deployment
            state.tigrbl_auth_settings = resolved_settings

        surface_router = self.surface_attacher(
            app,
            resolved_settings,
            deployment=deployment,
            diagnostics_prefix=self.diagnostics_prefix,
        )
        initializer = getattr(surface_router, "initialize", None)
        register_lifecycle(
            app,
            surface_initializer=initializer if callable(initializer) else None,
        )
        return app


def install(
    app: "TigrblApp",
    settings: object | None = None,
    *,
    surface_attacher: SurfaceAttacher,
) -> "TigrblApp":
    return TigrblAuthPlugin(
        settings=settings,
        surface_attacher=surface_attacher,
    ).install(app, settings=settings)


__all__ = ["SurfaceAttacher", "TigrblAuthPlugin", "install"]
