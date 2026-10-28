from __future__ import annotations

import inspect
from collections.abc import Awaitable, Callable
from typing import TypeAlias

from tigrbl import TigrblApp

from tba_runtime_identity_storage import initializeIdentityRuntimeTables
from tba_runtime_identity_storage.migrations import apply_all_async
from tba_runtime_identity.settings import settings
from tba_server_identity.admin_bootstrap import ensure_default_superuser_async
from tba_runtime_identity import RuntimeCapabilityAssembly


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
        app.state.tba_auth_runtime_assembly = assembly
        app.state.tba_auth_capability_registry = assembly.capabilities
        app.state.tba_protocol_reports = assembly.protocols


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
