from __future__ import annotations

import inspect
from collections.abc import Awaitable, Callable
from typing import TypeAlias

from tigrbl import TigrblApp

from tigrbl_identity_server.surfaces import PublicRouter as surface_api
from tigrbl_identity_storage_runtime import initializeIdentityRuntimeTables
from tigrbl_identity_storage_runtime.migrations import apply_all_async
from tigrbl_identity_runtime.settings import settings
from tigrbl_identity_admin.bootstrap import ensure_default_superuser_async
from tigrbl_identity_runtime import RuntimeCapabilityAssembly


AssemblyFactory: TypeAlias = Callable[
    [], RuntimeCapabilityAssembly | Awaitable[RuntimeCapabilityAssembly]
]


async def _startup(
    app: TigrblApp | None = None,
    assembly_factory: AssemblyFactory | None = None,
) -> None:
    await apply_all_async()
    initializeIdentityRuntimeTables()
    await ensure_default_superuser_async(settings)
    init = surface_api.initialize()
    if inspect.isawaitable(init):
        await init
    if assembly_factory is not None:
        assembly = assembly_factory()
        if inspect.isawaitable(assembly):
            assembly = await assembly
        if not isinstance(assembly, RuntimeCapabilityAssembly):
            raise TypeError(
                "runtime assembly factory must return RuntimeCapabilityAssembly"
            )
        if app is None or getattr(app, "state", None) is None:
            raise RuntimeError("runtime capability assembly requires application state")
        app.state.tigrbl_auth_runtime_assembly = assembly
        app.state.tigrbl_auth_capability_registry = assembly.capabilities
        app.state.tigrbl_auth_protocol_reports = assembly.protocols


def register_lifecycle(
    app: TigrblApp,
    *,
    assembly_factory: AssemblyFactory | None = None,
) -> None:
    async def startup() -> None:
        await _startup(app, assembly_factory)

    app.add_event_handler("startup", startup)


__all__ = ["AssemblyFactory", "register_lifecycle"]
