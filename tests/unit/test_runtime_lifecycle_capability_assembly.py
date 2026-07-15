from __future__ import annotations

from types import SimpleNamespace

import pytest

from tigrbl_capability import Capability
from tigrbl_identity_contracts.capabilities import (
    CapabilityDefinition,
    CapabilityOperation,
)
from tigrbl_identity_runtime import build_runtime_capability_assembly
from tigrbl_identity_server.api import lifecycle


@pytest.mark.asyncio
async def test_startup_attaches_assembly_after_storage_and_surface_initialization(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[str] = []

    class ProductSurfaceRouter:
        def initialize(self) -> None:
            calls.append("surface")

    async def migrate() -> None:
        calls.append("migrations")

    def tables() -> None:
        calls.append("tables")

    async def superuser(settings_obj: object) -> None:
        calls.append("superuser")

    def assembly():
        calls.append("assembly")
        return build_runtime_capability_assembly(
            build_providers=dict,
            build_storage_runtime=lambda providers: {},
            build_capabilities=lambda providers, storage: (
                Capability(
                    CapabilityDefinition("example", "1.0"),
                    operations={
                        "execute": CapabilityOperation(target=lambda: None),
                    },
                ),
            ),
            build_protocols=lambda registry: (),
        )

    app = SimpleNamespace(state=SimpleNamespace())
    monkeypatch.setattr(lifecycle, "apply_all_async", migrate)
    monkeypatch.setattr(lifecycle, "initializeIdentityRuntimeTables", tables)
    monkeypatch.setattr(lifecycle, "ensure_default_superuser_async", superuser)
    monkeypatch.setattr(lifecycle, "surface_api", ProductSurfaceRouter())

    await lifecycle._startup(app, assembly)

    assert calls == ["migrations", "tables", "superuser", "surface", "assembly"]
    assert app.state.tigrbl_auth_capability_registry.capability_ids() == ("example",)
    assert app.state.tigrbl_auth_protocol_reports == ()


@pytest.mark.asyncio
async def test_startup_rejects_an_invalid_assembly_factory(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def noop(*args: object, **kwargs: object) -> None:
        return None

    monkeypatch.setattr(lifecycle, "apply_all_async", noop)
    monkeypatch.setattr(lifecycle, "initializeIdentityRuntimeTables", lambda: None)
    monkeypatch.setattr(lifecycle, "ensure_default_superuser_async", noop)
    monkeypatch.setattr(lifecycle, "surface_api", SimpleNamespace(initialize=lambda: None))

    with pytest.raises(TypeError, match="RuntimeCapabilityAssembly"):
        await lifecycle._startup(
            SimpleNamespace(state=SimpleNamespace()),
            lambda: object(),
        )
