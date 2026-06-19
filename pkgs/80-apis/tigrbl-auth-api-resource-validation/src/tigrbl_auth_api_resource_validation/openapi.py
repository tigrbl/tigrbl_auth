"""OpenAPI affordances for the resource-validation API package."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
from typing import Any, Callable


_INTROSPECTION_BODY = {
    "required": True,
    "content": {
        "application/x-www-form-urlencoded": {
            "schema": {
                "type": "object",
                "required": ["token"],
                "properties": {
                    "token": {"type": "string"},
                    "token_type_hint": {
                        "type": "string",
                        "enum": ["access_token", "refresh_token"],
                    },
                    "client_id": {"type": "string"},
                    "client_secret": {"type": "string", "format": "password"},
                },
            },
            "example": {
                "token": "<access-token>",
                "token_type_hint": "access_token",
                "client_id": "<resource-server-client-id>",
                "client_secret": "<resource-server-client-secret>",
            },
        }
    },
}


def _operation(openapi: dict[str, Any], path: str, method: str) -> dict[str, Any]:
    return openapi.setdefault("paths", {}).setdefault(path, {}).setdefault(method, {})


def patch_resource_validation_openapi(app: object) -> object:
    """Patch generated OpenAPI for validation protocol endpoints."""
    target = getattr(app, "app", app)
    original_openapi: Callable[[], dict[str, Any]] = target.openapi

    def resource_validation_openapi() -> dict[str, Any]:
        cached = getattr(target, "openapi_schema", None)
        if cached:
            return cached

        openapi = original_openapi()
        if "/introspect" in openapi.get("paths", {}):
            _operation(openapi, "/introspect", "post")["requestBody"] = deepcopy(
                _INTROSPECTION_BODY
            )
        setattr(target, "openapi_schema", openapi)
        return openapi

    target.openapi = resource_validation_openapi
    if target is not app:
        app.openapi = resource_validation_openapi

    routes = getattr(target, "_routes", None)
    if isinstance(routes, list):
        from tigrbl_concrete._concrete._response import Response

        def _openapi_handler(request: Any) -> Response:
            return Response.json(resource_validation_openapi())

        patched_routes = []
        for route in routes:
            path = str(getattr(route, "path_template", None) or getattr(route, "path", ""))
            methods = set(getattr(route, "methods", ()) or ())
            if path == "/openapi.json" and "GET" in methods:
                patched_routes.append(replace(route, handler=_openapi_handler))
            else:
                patched_routes.append(route)
        routes[:] = patched_routes
    return ResourceValidationOpenAPIGate(app)


class ResourceValidationOpenAPIGate:
    """ASGI wrapper that serves the patched validation OpenAPI document."""

    def __init__(self, app: object) -> None:
        self.app = app

    def __getattr__(self, name: str) -> Any:
        return getattr(self.app, name)

    def openapi(self) -> dict[str, Any]:
        return self.app.openapi()

    async def __call__(self, scope: dict[str, Any], receive: Any, send: Any) -> None:
        if (
            scope.get("type") == "http"
            and str(scope.get("method", "")).upper() == "GET"
            and scope.get("path") == "/openapi.json"
        ):
            from tigrbl_concrete._concrete._response import Response

            await Response.json(self.openapi())(scope, receive, send)
            return
        await self.app(scope, receive, send)


__all__ = ["patch_resource_validation_openapi"]
