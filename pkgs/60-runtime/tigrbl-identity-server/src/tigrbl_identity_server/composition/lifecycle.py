from __future__ import annotations

import inspect
from collections.abc import Awaitable, Callable
from typing import TypeAlias

from tigrbl import TigrblApp

from tigrbl_identity_storage_runtime import initializeIdentityRuntimeTables
from tigrbl_identity_storage_runtime.migrations import apply_all_async
from tigrbl_identity_runtime.settings import settings
from tigrbl_identity_server.admin_bootstrap import ensure_default_superuser_async
from tigrbl_identity_runtime import RuntimeCapabilityAssembly


AssemblyFactory: TypeAlias = Callable[
    [], RuntimeCapabilityAssembly | Awaitable[RuntimeCapabilityAssembly]
]
SurfaceInitializer: TypeAlias = Callable[[], object]


async def _startup(
    app: TigrblApp | None = None,
    assembly_factory: AssemblyFactory | None = None,
    surface_initializer: SurfaceInitializer | None = None,
) -> None:
    await apply_all_async()
    initializeIdentityRuntimeTables()
    await ensure_default_superuser_async(settings)
    if surface_initializer is not None:
        initialized = surface_initializer()
        if inspect.isawaitable(initialized):
            await initialized
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
    surface_initializer: SurfaceInitializer | None = None,
) -> None:
    async def startup() -> None:
        await _startup(app, assembly_factory, surface_initializer)

    app.add_event_handler("startup", startup)


__all__ = ["AssemblyFactory", "SurfaceInitializer", "register_lifecycle"]
