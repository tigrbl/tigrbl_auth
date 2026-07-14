"""ASGI entrypoint for the platform admin Tigrbl Auth API surface."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, Awaitable, Callable

from tigrbl_auth.api.products import build_product_app
from tigrbl_auth.runtime import LazyASGIApplication
from tigrbl_auth_api_platform_admin.identities import api as identity_api
from tigrbl_auth_api_platform_admin.realms import api as realm_api

if TYPE_CHECKING:
    from tigrbl import TigrblApp

PRODUCT_SURFACE = "platform-admin-api"
DEFAULT_CORS_ORIGINS = ("http://localhost:3011", "http://127.0.0.1:3011")


class PlatformAdminCors:
    """Small ASGI CORS wrapper for the standalone platform admin UIX demo."""

    def __init__(self, app: Any, origins: tuple[str, ...] = DEFAULT_CORS_ORIGINS) -> None:
        self.app = app
        self.origins = origins

    def __getattr__(self, name: str) -> Any:
        return getattr(self.app, name)

    async def __call__(
        self,
        scope: dict[str, Any],
        receive: Callable[[], Awaitable[dict[str, Any]]],
        send: Callable[[dict[str, Any]], Awaitable[None]],
    ) -> None:
        if scope.get("type") != "http":
            await self.app(scope, receive, send)
            return

        headers = {
            key.decode("latin-1").lower(): value.decode("latin-1")
            for key, value in scope.get("headers", [])
        }
        origin = headers.get("origin")
        allowed_origin = origin if origin in self.origins else None

        if str(scope.get("method", "")).upper() == "OPTIONS" and allowed_origin:
            await send(
                {
                    "type": "http.response.start",
                    "status": 204,
                    "headers": self._cors_headers(allowed_origin)
                    + [
                        (b"access-control-allow-methods", b"GET,POST,PATCH,DELETE,OPTIONS"),
                        (
                            b"access-control-allow-headers",
                            headers.get(
                                "access-control-request-headers",
                                "content-type,authorization,x-api-key",
                            ).encode("latin-1"),
                        ),
                        (b"content-length", b"0"),
                    ],
                }
            )
            await send({"type": "http.response.body", "body": b""})
            return

        async def cors_send(message: dict[str, Any]) -> None:
            if message.get("type") == "http.response.start" and allowed_origin:
                message = dict(message)
                response_headers = list(message.get("headers", []))
                response_headers.extend(self._cors_headers(allowed_origin))
                message["headers"] = response_headers
            await send(message)

        await self.app(scope, receive, cors_send)

    @staticmethod
    def _cors_headers(origin: str) -> list[tuple[bytes, bytes]]:
        return [
            (b"access-control-allow-origin", origin.encode("latin-1")),
            (b"access-control-allow-credentials", b"true"),
            (b"vary", b"Origin"),
        ]


def _default_settings() -> object:
    from tigrbl_auth.config.settings import Settings

    settings = Settings()
    env_overrides = {
        "issuer": os.environ.get("AUTHN_ISSUER"),
        "protected_resource_identifier": os.environ.get(
            "TIGRBL_AUTH_PROTECTED_RESOURCE_IDENTIFIER"
        ),
        "deployment_profile": os.environ.get("TIGRBL_AUTH_PROFILE"),
        "require_tls": os.environ.get("TIGRBL_AUTH_REQUIRE_TLS"),
        "admin_api_key": os.environ.get("TIGRBL_AUTH_ADMIN_API_KEY"),
        "admin_api_key_dir": os.environ.get("TIGRBL_AUTH_ADMIN_API_KEY_DIR"),
    }
    for name, value in env_overrides.items():
        if value in {None, ""}:
            continue
        current = getattr(settings, name, None)
        if isinstance(current, bool):
            value = str(value).lower() in {"1", "true", "yes", "on"}
        setattr(settings, name, value)
    return settings


def build_app(settings_obj: object | None = None) -> "TigrblApp":
    if settings_obj is None:
        settings_obj = _default_settings()
    app = build_product_app(PRODUCT_SURFACE, settings_obj)
    app.include_router(realm_api)
    app.include_router(identity_api)
    app.admin_path_prefixes = tuple(
        dict.fromkeys((*app.admin_path_prefixes, "/admin/identities"))
    )
    return PlatformAdminCors(app)


app = LazyASGIApplication(build_app)

__all__ = ["PRODUCT_SURFACE", "app", "build_app"]
