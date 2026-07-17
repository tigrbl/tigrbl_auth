from __future__ import annotations

import importlib

from tigrbl_auth_backend_app_core.surfaces.revocation_surface import (
    include_revocation_endpoint,
    router,
)


def test_runtime_surface_mounts_layer_80_revocation_carrier() -> None:
    surface_api = importlib.import_module(
        "tigrbl_auth_backend_app_core.surfaces.surface_api"
    )
    binding = next(
        item
        for item in surface_api.PUBLIC_PUBLISHER_BINDINGS
        if item["mount_group"] == "revoke"
    )

    assert binding["include"] is include_revocation_endpoint
    assert any(getattr(route, "path", None) == "/revoke" for route in router.routes)
