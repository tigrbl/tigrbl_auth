"""ASGI entrypoint for the My Account Tigrbl Auth backend application."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, Awaitable, Callable

from tigrbl_auth_backend_app_core import build_product_app
from tigrbl_auth_backend_app_my_account.contract import MY_ACCOUNT_BACKEND_APP_CONTRACT
from tigrbl_auth.runtime import LazyASGIApplication
from tigrbl_auth_backend_app_my_account.openapi import patch_my_account_openapi
from tigrbl_auth_backend_app_my_account.routes import router as account_router

if TYPE_CHECKING:
    from tigrbl import TigrblApp

PRODUCT_SURFACE = "my-account-app"
DEFAULT_CORS_ORIGINS = ("http://localhost:3019", "http://127.0.0.1:3019")


class MyAccountCors:
    """Small ASGI CORS wrapper for the standalone My Account/UIX demo surface."""

    def __init__(
        self, app: Any, origins: tuple[str, ...] = DEFAULT_CORS_ORIGINS
    ) -> None:
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
                        (
                            b"access-control-allow-methods",
                            b"GET,PATCH,POST,DELETE,OPTIONS",
                        ),
                        (
                            b"access-control-allow-headers",
                            headers.get(
                                "access-control-request-headers",
                                "content-type,authorization",
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
        "session_cookie_force_secure": os.environ.get(
            "TIGRBL_AUTH_SESSION_COOKIE_FORCE_SECURE"
        ),
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
    app = build_product_app(
        PRODUCT_SURFACE, settings_obj, contract=MY_ACCOUNT_BACKEND_APP_CONTRACT
    )
    app.include_router(account_router)
    app = patch_my_account_openapi(app)
    return MyAccountCors(app)


app = LazyASGIApplication(build_app)

__all__ = ["PRODUCT_SURFACE", "app", "build_app"]
