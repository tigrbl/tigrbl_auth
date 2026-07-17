"""Layer-90 host-application plugin with HTTP surface ownership."""

from __future__ import annotations

from typing import TYPE_CHECKING

from tigrbl_auth_plugin import TigrblAuthPlugin as RuntimePlugin

from .surfaces import attach_runtime_surfaces

if TYPE_CHECKING:
    from tigrbl import TigrblApp


class TigrblAuthBackendAppPlugin(RuntimePlugin):
    def __init__(
        self,
        *,
        diagnostics_prefix: str = "/system",
        settings: object | None = None,
    ) -> None:
        super().__init__(
            surface_attacher=attach_runtime_surfaces,
            diagnostics_prefix=diagnostics_prefix,
            settings=settings,
        )


def install(app: "TigrblApp", settings: object | None = None) -> "TigrblApp":
    return TigrblAuthBackendAppPlugin(settings=settings).install(
        app,
        settings=settings,
    )


__all__ = ["TigrblAuthBackendAppPlugin", "install"]
