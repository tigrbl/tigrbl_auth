from __future__ import annotations

import inspect

from tigrbl import TigrblApp

from tigrbl_identity_server.api.surfaces import surface_api
from tigrbl_identity_storage.migrations import apply_all_async
from tigrbl_identity_runtime.settings import settings
from tigrbl_identity_admin.bootstrap import ensure_default_superuser_async


async def _startup() -> None:
    await apply_all_async()
    await ensure_default_superuser_async(settings)
    init = surface_api.initialize()
    if inspect.isawaitable(init):
        await init


def register_lifecycle(app: TigrblApp) -> None:
    app.add_event_handler("startup", _startup)
