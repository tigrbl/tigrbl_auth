"""OpenAPI affordances for the My Account API package."""

from __future__ import annotations

from dataclasses import replace
from typing import Any, Callable


def patch_my_account_openapi(app: object) -> object:
    """Patch generated OpenAPI metadata for the My Account surface."""
    target = getattr(app, "app", app)
    original_openapi: Callable[[], dict[str, Any]] = target.openapi

    def my_account_openapi() -> dict[str, Any]:
        cached = getattr(target, "openapi_schema", None)
        if cached:
            return cached
        openapi = original_openapi()
        openapi["title"] = "tigrbl-auth-api-my-account"
        for path, methods in openapi.get("paths", {}).items():
            if path.startswith("/account/"):
                for operation in methods.values():
                    operation["tags"] = ["My Account"]
        setattr(target, "openapi_schema", openapi)
        return openapi

    target.openapi = my_account_openapi
    if target is not app:
        app.openapi = my_account_openapi

    routes = getattr(target, "_routes", None)
    if isinstance(routes, list):
        from tigrbl_concrete._concrete._response import Response

        def _openapi_handler(request: Any) -> Response:
            return Response.json(my_account_openapi())

        patched_routes = []
        for route in routes:
            path = str(getattr(route, "path_template", None) or getattr(route, "path", ""))
            methods = set(getattr(route, "methods", ()) or ())
            if path == "/openapi.json" and "GET" in methods:
                patched_routes.append(replace(route, handler=_openapi_handler))
            else:
                patched_routes.append(route)
        routes[:] = patched_routes
    return app


__all__ = ["patch_my_account_openapi"]
