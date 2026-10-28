"""HTTP carrier binding for the OpenID Connect UserInfo endpoint."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any, TypeAlias

from tigrbl import Depends, Request, TigrblApp, TigrblRouter


DatabaseDependency: TypeAlias = Callable[..., object]
UserInfoRequestTarget: TypeAlias = Callable[..., Any | Awaitable[Any]]


def build_userinfo_router(
    *,
    userinfo_request: UserInfoRequestTarget,
    get_db: DatabaseDependency,
) -> TigrblRouter:
    """Build the GET carrier around injected UserInfo orchestration."""

    router = TigrblRouter()

    @router.route("/userinfo", methods=["GET"], response_model=None)
    async def userinfo(request: Request, db: object = Depends(get_db)) -> Any:
        return await userinfo_request(request=request, db=db)

    return router


def include_userinfo_endpoint(
    app: TigrblApp,
    router: TigrblRouter,
    *,
    enabled: bool = True,
) -> None:
    """Mount the UserInfo carrier once when selected by composition."""

    routes = getattr(getattr(app, "router", None), "routes", ())
    if enabled and not any(
        (getattr(route, "path", None) or getattr(route, "path_template", None))
        == "/userinfo"
        for route in routes
    ):
        app.include_router(router)


__all__ = [
    "DatabaseDependency",
    "UserInfoRequestTarget",
    "build_userinfo_router",
    "include_userinfo_endpoint",
]
