from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from tigrbl_auth.config.deployment import ResolvedDeployment, resolve_deployment

if TYPE_CHECKING:
    from tigrbl import TigrblApp


@dataclass(slots=True, kw_only=True)
class TigrblAuthPlugin:
    """Install the tigrbl_auth surfaces into an existing ``TigrblApp``."""

    rpc_prefix: str = "/rpc"
    diagnostics_prefix: str = "/system"
    settings: object | None = None

    def resolve_plugin_deployment(self, settings: object | None = None) -> ResolvedDeployment:
        resolved_settings = settings if settings is not None else self.settings
        return resolve_deployment(resolved_settings, runtime_style="plugin")

    def install(self, app: "TigrblApp", settings: object | None = None) -> "TigrblApp":
        resolved_settings = settings if settings is not None else self.settings
        deployment = self.resolve_plugin_deployment(resolved_settings)

        from tigrbl_auth.api.lifecycle import register_lifecycle
        from tigrbl_auth.api.surfaces import attach_runtime_surfaces

        state = getattr(app, "state", None)
        if state is not None:
            state.tigrbl_auth_deployment = deployment
            state.tigrbl_auth_settings = resolved_settings

        attach_runtime_surfaces(
            app,
            resolved_settings,
            deployment=deployment,
            rpc_prefix=self.rpc_prefix,
            diagnostics_prefix=self.diagnostics_prefix,
        )
        register_lifecycle(app)
        return app



def install(app: "TigrblApp", settings: object | None = None) -> "TigrblApp":
    return TigrblAuthPlugin(settings=settings).install(app, settings=settings)


__all__ = ["TigrblAuthPlugin", "install"]
