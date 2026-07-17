"""HTTP carrier binding for the OAuth token endpoint."""

from __future__ import annotations

from collections.abc import Awaitable, Callable, Mapping
from typing import Any, TypeAlias

from tigrbl import Depends, Request, TigrblApp, TigrblRouter
from tigrbl_auth_protocol_oauth.schemas import TokenPair


DatabaseDependency: TypeAlias = Callable[..., object]
TokenRequestTarget: TypeAlias = Callable[
    ...,
    Mapping[str, object] | Any | Awaitable[Mapping[str, object] | Any],
]


def build_token_router(
    *,
    token_request: TokenRequestTarget,
    get_db: DatabaseDependency,
) -> TigrblRouter:
    """Build the POST carrier around an injected token-request processor."""

    router = TigrblRouter()

    @router.route("/token", methods=["POST"], response_model=TokenPair)
    async def token(request: Request, db: object = Depends(get_db)) -> Any:
        return await token_request(request=request, db=db)

    return router


def include_token_endpoint(
    app: TigrblApp,
    router: TigrblRouter,
    *,
    enabled: bool = True,
) -> None:
    """Mount the token carrier once when enabled by runtime composition."""

    path = "/token"
    routes = getattr(getattr(app, "router", None), "routes", ())
    if enabled and not any(
        (getattr(route, "path", None) or getattr(route, "path_template", None))
        == path
        for route in routes
    ):
        app.include_router(router)


__all__ = [
    "DatabaseDependency",
    "TokenRequestTarget",
    "build_token_router",
    "include_token_endpoint",
]
