from __future__ import annotations

from tigrbl import TigrblRouter


def test_identity_server_exports_named_tigrbl_routers() -> None:
    from tigrbl_identity_server.surfaces import AdminRouter, PublicRouter, surface_api

    assert isinstance(AdminRouter, TigrblRouter)
    assert isinstance(PublicRouter, TigrblRouter)
    assert surface_api is PublicRouter
    assert len(getattr(AdminRouter, "_routes", ())) > 0
    assert len(getattr(PublicRouter, "_routes", ())) > 0


def test_identity_server_compatibility_surfaces_share_public_router() -> None:
    from tigrbl_identity_server.api.surfaces import PublicRouter as api_public_router
    from tigrbl_identity_server.api.surfaces import surface_api as api_surface_api
    from tigrbl_identity_server.routers.surface import PublicRouter as legacy_public_router
    from tigrbl_identity_server.routers.surface import surface_api as legacy_surface_api
    from tigrbl_identity_server.surfaces import PublicRouter

    assert api_public_router is PublicRouter
    assert api_surface_api is PublicRouter
    assert legacy_public_router is PublicRouter
    assert legacy_surface_api is PublicRouter
