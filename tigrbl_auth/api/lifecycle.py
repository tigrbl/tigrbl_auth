from __future__ import annotations

import inspect

from tigrbl import TigrblApp

from tigrbl_auth.api.surfaces import surface_api
from tigrbl_auth.migrations import apply_all_async
from tigrbl_auth.config.settings import settings
from tigrbl_auth.services.admin_identity_bootstrap import ensure_default_superuser_async


async def _startup(app: TigrblApp, settings_obj: object | None = None) -> None:
    await apply_all_async()
    await ensure_default_superuser_async(settings_obj or settings)
    state = getattr(app, "state", None)
    router = getattr(state, "tigrbl_auth_surface_router", None) if state else None
    init = (router or surface_api).initialize()
    if inspect.isawaitable(init):
        await init


def register_lifecycle(app: TigrblApp, settings_obj: object | None = None) -> None:
    async def _run_startup() -> None:
        await _startup(app, settings_obj)

    app.add_event_handler("startup", _run_startup)
