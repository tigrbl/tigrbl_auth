from __future__ import annotations

import importlib

from tigrbl_identity_server.introspection_surface import (
    include_introspection_endpoint,
    router,
)


def test_runtime_surface_mounts_layer_80_introspection_carrier() -> None:
    surface_api = importlib.import_module(
        "tigrbl_identity_server._surfaces.surface_api"
    )
    binding = next(
        item
        for item in surface_api.PUBLIC_PUBLISHER_BINDINGS
        if item["mount_group"] == "introspection"
    )

    assert binding["include"] is include_introspection_endpoint
    assert any(
        getattr(route, "path", None) == "/introspect" for route in router.routes
    )
