"""Layer-90 host-application plugin with HTTP surface ownership."""

from __future__ import annotations

from typing import TYPE_CHECKING

from tba_plugin_tigrbl import TbaPlugin as RuntimePlugin

from .surfaces import attach_runtime_surfaces

if TYPE_CHECKING:
    from tigrbl import TigrblApp


class TbaBackendAppPlugin(RuntimePlugin):
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
    return TbaBackendAppPlugin(settings=settings).install(
        app,
        settings=settings,
    )


__all__ = ["TbaBackendAppPlugin", "install"]
