from __future__ import annotations

from tigrbl import TigrblApp, TigrblRouter
from tigrbl_identity_runtime import standards_manifest

api = TigrblRouter()


@api.route("/standards", methods=["GET"], include_in_schema=True, tags=["standards"])
async def get_standards_manifest() -> dict[str, object]:
    return {"standards": standards_manifest()}


def include_standards_manifest(app: TigrblApp) -> None:
    path = "/standards"
    routes = getattr(getattr(app, "router", app), "routes", ())
    if not any(
        (getattr(route, "path", None) or getattr(route, "path_template", None)) == path
        for route in routes
    ):
        app.include_router(api)


__all__ = ["api", "get_standards_manifest", "include_standards_manifest"]
