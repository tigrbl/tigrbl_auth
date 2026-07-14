"""HTTP carrier binding for interactive identity session login."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any, TypeAlias

from pydantic import BaseModel, constr
from tigrbl import Depends, Request, TigrblApp, TigrblRouter
from tigrbl_auth_protocol_oauth.schemas import TokenPair


class CredsIn(BaseModel):
    identifier: constr(strip_whitespace=True, min_length=3, max_length=120)
    password: constr(min_length=8, max_length=256)


DatabaseDependency: TypeAlias = Callable[..., object]
LoginRequestTarget: TypeAlias = Callable[..., Any | Awaitable[Any]]


def build_login_router(
    *,
    login_request: LoginRequestTarget,
    get_db: DatabaseDependency,
) -> TigrblRouter:
    """Build the POST login carrier around injected runtime orchestration."""

    router = TigrblRouter()

    @router.route("/login", methods=["POST"], response_model=TokenPair)
    async def login(
        request: Request,
        creds: CredsIn | None = None,
        db: object = Depends(get_db),
    ) -> Any:
        if creds is None:
            creds = CredsIn.model_validate(await request.json() or {})
        return await login_request(
            request=request,
            db=db,
            identifier=creds.identifier,
            password=creds.password,
        )

    return router


def include_login_endpoint(
    app: TigrblApp,
    router: TigrblRouter,
    *,
    enabled: bool = True,
) -> None:
    """Mount the login carrier once when selected by composition."""

    routes = getattr(getattr(app, "router", None), "routes", ())
    if enabled and not any(
        (getattr(route, "path", None) or getattr(route, "path_template", None))
        == "/login"
        for route in routes
    ):
        app.include_router(router)


__all__ = [
    "CredsIn",
    "DatabaseDependency",
    "LoginRequestTarget",
    "build_login_router",
    "include_login_endpoint",
]
