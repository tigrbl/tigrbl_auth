"""HTTP carrier binding for OpenID Connect RP-Initiated Logout."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any, TypeAlias

from tigrbl import Depends, Request, TigrblApp, TigrblRouter


DatabaseDependency: TypeAlias = Callable[..., object]
LogoutRequestTarget: TypeAlias = Callable[..., Any | Awaitable[Any]]


def build_logout_router(
    *,
    logout_request: LogoutRequestTarget,
    get_db: DatabaseDependency,
) -> TigrblRouter:
    """Build GET and POST carriers around injected logout orchestration."""

    router = TigrblRouter()

    @router.route("/logout", methods=["GET", "POST"], response_model=None)
    async def logout(request: Request, db: object = Depends(get_db)) -> Any:
        return await logout_request(request=request, db=db)

    return router


def include_logout_endpoint(
    app: TigrblApp,
    router: TigrblRouter,
    *,
    enabled: bool = True,
) -> None:
    """Mount the logout carrier once when selected by composition."""

    routes = getattr(getattr(app, "router", None), "routes", ())
    if enabled and not any(
        (getattr(route, "path", None) or getattr(route, "path_template", None))
        == "/logout"
        for route in routes
    ):
        app.include_router(router)


__all__ = [
    "DatabaseDependency",
    "LogoutRequestTarget",
    "build_logout_router",
    "include_logout_endpoint",
]
