"""OpenAPI affordances for the public API package.

The shared runtime intentionally hand-parses several OAuth/OIDC endpoints so it
can accept exact protocol wire formats. Tigrbl cannot infer request bodies from
those handlers, so this package overlays the public front-door documentation.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
from typing import Any, Callable


_LOGIN_BODY = {
    "required": True,
    "content": {
        "application/json": {
            "schema": {"$ref": "#/components/schemas/CredsIn"},
            "example": {"identifier": "admin", "password": "AdminPass123!"},
        }
    },
}

_REGISTER_BODY = {
    "required": True,
    "content": {
        "application/json": {
            "schema": {"$ref": "#/components/schemas/DynamicClientRegistrationIn"},
            "example": {
                "tenant_slug": "public",
                "redirect_uris": ["http://127.0.0.1:8080/callback"],
                "grant_types": ["authorization_code", "refresh_token", "password"],
                "response_types": ["code"],
                "token_endpoint_auth_method": "client_secret_post",
                "client_name": "Local dev client",
                "scope": "openid profile email",
            },
        }
    },
}

_TOKEN_BODY = {
    "required": True,
    "content": {
        "application/x-www-form-urlencoded": {
            "schema": {
                "type": "object",
                "required": ["grant_type", "client_id"],
                "properties": {
                    "grant_type": {
                        "type": "string",
                        "enum": [
                            "authorization_code",
                            "client_credentials",
                            "password",
                            "refresh_token",
                        ],
                    },
                    "client_id": {"type": "string"},
                    "client_secret": {"type": "string"},
                    "username": {"type": "string"},
                    "password": {"type": "string", "format": "password"},
                    "scope": {"type": "string"},
                    "code": {"type": "string"},
                    "redirect_uri": {"type": "string", "format": "uri"},
                    "code_verifier": {"type": "string"},
                    "refresh_token": {"type": "string"},
                    "resource": {"type": "string"},
                },
            },
            "examples": {
                "password": {
                    "summary": "Password grant after dynamic client registration",
                    "value": {
                        "grant_type": "password",
                        "client_id": "<registered-client-id>",
                        "client_secret": "<registered-client-secret>",
                        "username": "admin",
                        "password": "AdminPass123!",
                        "scope": "openid profile email",
                    },
                },
                "authorization_code": {
                    "summary": "Authorization code exchange",
                    "value": {
                        "grant_type": "authorization_code",
                        "client_id": "<registered-client-id>",
                        "client_secret": "<registered-client-secret>",
                        "code": "<authorization-code>",
                        "redirect_uri": "http://127.0.0.1:8080/callback",
                        "code_verifier": "<pkce-code-verifier>",
                    },
                },
            },
        }
    },
}

_LOGOUT_BODY = {
    "required": False,
    "content": {
        "application/json": {
            "schema": {"$ref": "#/components/schemas/LogoutIn"},
            "example": {"client_id": "<registered-client-id>", "state": "dev-state"},
        }
    },
}

_TOKEN_REFERENCE_BODY = {
    "required": True,
    "content": {
        "application/x-www-form-urlencoded": {
            "schema": {
                "type": "object",
                "required": ["token"],
                "properties": {
                    "token": {"type": "string"},
                    "token_type_hint": {"type": "string"},
                    "client_id": {"type": "string"},
                    "client_secret": {"type": "string"},
                },
            }
        }
    },
}

_AUTHORIZE_PARAMS = [
    {
        "name": "response_type",
        "in": "query",
        "required": True,
        "schema": {"type": "string", "default": "code"},
    },
    {
        "name": "client_id",
        "in": "query",
        "required": True,
        "schema": {"type": "string"},
    },
    {
        "name": "redirect_uri",
        "in": "query",
        "required": True,
        "schema": {
            "type": "string",
            "format": "uri",
            "default": "http://127.0.0.1:8080/callback",
        },
    },
    {
        "name": "scope",
        "in": "query",
        "required": False,
        "schema": {"type": "string", "default": "openid profile email"},
    },
    {
        "name": "state",
        "in": "query",
        "required": False,
        "schema": {"type": "string", "default": "dev-state"},
    },
    {
        "name": "nonce",
        "in": "query",
        "required": False,
        "schema": {"type": "string", "default": "dev-nonce"},
    },
    {
        "name": "code_challenge",
        "in": "query",
        "required": True,
        "schema": {
            "type": "string",
            "default": "E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM",
        },
    },
    {
        "name": "code_challenge_method",
        "in": "query",
        "required": True,
        "schema": {"type": "string", "enum": ["S256"], "default": "S256"},
    },
]


def _ensure_schema(openapi: dict[str, Any], name: str, schema: dict[str, Any]) -> None:
    components = openapi.setdefault("components", {})
    schemas = components.setdefault("schemas", {})
    schemas.setdefault(name, schema)


def _operation(openapi: dict[str, Any], path: str, method: str) -> dict[str, Any]:
    return openapi.setdefault("paths", {}).setdefault(path, {}).setdefault(method, {})


def _replace_params(operation: dict[str, Any], params: list[dict[str, Any]]) -> None:
    existing = operation.get("parameters") or []
    preserved = [
        param
        for param in existing
        if (param.get("in"), param.get("name"))
        not in {(item["in"], item["name"]) for item in params}
    ]
    operation["parameters"] = preserved + deepcopy(params)


def patch_public_openapi(app: object) -> object:
    """Patch generated OpenAPI for public protocol endpoints."""
    target = getattr(app, "app", app)
    original_openapi: Callable[[], dict[str, Any]] = target.openapi

    def public_openapi() -> dict[str, Any]:
        cached = getattr(target, "openapi_schema", None)
        if cached:
            return cached

        openapi = original_openapi()
        _ensure_schema(
            openapi,
            "CredsIn",
            {
                "type": "object",
                "required": ["identifier", "password"],
                "properties": {
                    "identifier": {"type": "string", "minLength": 3},
                    "password": {"type": "string", "format": "password", "minLength": 8},
                },
            },
        )
        _ensure_schema(
            openapi,
            "DynamicClientRegistrationIn",
            {
                "type": "object",
                "required": ["redirect_uris"],
                "properties": {
                    "tenant_slug": {"type": "string", "default": "public"},
                    "redirect_uris": {
                        "type": "array",
                        "items": {"type": "string", "format": "uri"},
                    },
                    "grant_types": {
                        "type": "array",
                        "items": {"type": "string"},
                        "default": ["authorization_code"],
                    },
                    "response_types": {
                        "type": "array",
                        "items": {"type": "string"},
                        "default": ["code"],
                    },
                    "token_endpoint_auth_method": {
                        "type": "string",
                        "default": "client_secret_basic",
                    },
                    "scope": {"type": "string"},
                    "client_name": {"type": "string"},
                },
            },
        )
        _ensure_schema(
            openapi,
            "LogoutIn",
            {
                "type": "object",
                "properties": {
                    "id_token_hint": {"type": "string"},
                    "post_logout_redirect_uri": {"type": "string", "format": "uri"},
                    "state": {"type": "string"},
                    "sid": {"type": "string"},
                    "client_id": {"type": "string"},
                },
            },
        )

        _operation(openapi, "/login", "post")["requestBody"] = deepcopy(_LOGIN_BODY)
        _operation(openapi, "/register", "post")["requestBody"] = deepcopy(
            _REGISTER_BODY
        )
        _operation(openapi, "/token", "post")["requestBody"] = deepcopy(_TOKEN_BODY)
        _operation(openapi, "/logout", "post")["requestBody"] = deepcopy(_LOGOUT_BODY)
        _operation(openapi, "/revoke", "post")["requestBody"] = deepcopy(
            _TOKEN_REFERENCE_BODY
        )
        if "/introspect" in openapi.get("paths", {}):
            _operation(openapi, "/introspect", "post")["requestBody"] = deepcopy(
                _TOKEN_REFERENCE_BODY
            )
        if "/authorize" in openapi.get("paths", {}):
            _replace_params(_operation(openapi, "/authorize", "get"), _AUTHORIZE_PARAMS)

        setattr(target, "openapi_schema", openapi)
        return openapi

    target.openapi = public_openapi
    if target is not app:
        app.openapi = public_openapi

    routes = getattr(target, "_routes", None)
    if isinstance(routes, list):
        from tigrbl_concrete._concrete._response import Response

        def _openapi_handler(request: Any) -> Response:
            return Response.json(public_openapi())

        patched_routes = []
        for route in routes:
            path = str(getattr(route, "path_template", None) or getattr(route, "path", ""))
            methods = set(getattr(route, "methods", ()) or ())
            if path == "/openapi.json" and "GET" in methods:
                patched_routes.append(replace(route, handler=_openapi_handler))
            else:
                patched_routes.append(route)
        routes[:] = patched_routes
    return PublicOpenAPIGate(app)


__all__ = ["patch_public_openapi"]
class PublicOpenAPIGate:
    """ASGI wrapper that serves the patched public OpenAPI document."""

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
