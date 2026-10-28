"""HTTP carrier binding for RFC 8693 token exchange."""

from __future__ import annotations

import inspect
from collections.abc import Awaitable, Callable, Mapping
from typing import TypeAlias

from tigrbl import Request, TigrblApp, TigrblRouter
from tigrbl.core.crud.params import Header


TokenExchangeTarget: TypeAlias = Callable[
    [Request, str | None],
    Mapping[str, object] | Awaitable[Mapping[str, object]],
]


def build_token_exchange_router(
    *,
    token_exchange_request: TokenExchangeTarget,
) -> TigrblRouter:
    """Build the RFC 8693 POST carrier around injected orchestration."""

    router = TigrblRouter()

    @router.route("/token/exchange", methods=["POST"])
    async def token_exchange(
        request: Request,
        dpop: str | None = Header(None, alias="DPoP"),
    ) -> Mapping[str, object]:
        value = token_exchange_request(request, dpop)
        if inspect.isawaitable(value):
            value = await value
        return value

    return router


def include_token_exchange_endpoint(
    app: TigrblApp,
    router: TigrblRouter,
    *,
    enabled: bool = True,
) -> None:
    """Mount the token-exchange carrier once when enabled."""

    path = "/token/exchange"
    routes = getattr(getattr(app, "router", None), "routes", ())
    if enabled and not any(
        (getattr(route, "path", None) or getattr(route, "path_template", None))
        == path
        for route in routes
    ):
        app.include_router(router)


__all__ = [
    "TokenExchangeTarget",
    "build_token_exchange_router",
    "include_token_exchange_endpoint",
]
