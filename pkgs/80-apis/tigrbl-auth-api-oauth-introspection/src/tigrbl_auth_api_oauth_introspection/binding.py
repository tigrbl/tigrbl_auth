"""HTTP carrier binding for the RFC 7662 introspection operation."""

from __future__ import annotations

import inspect
from collections.abc import Awaitable, Callable, Mapping
from typing import TypeAlias
from urllib.parse import parse_qs

from tigrbl import Depends, Request, TigrblApp, TigrblRouter
from tigrbl.runtime.status import HTTPException, status
from tigrbl_auth_protocol_oauth.schemas import IntrospectOut
from tigrbl_auth_protocol_oauth.standards.introspection import (
    IntrospectionDisabledError,
    RFC7662IntrospectionService,
)


DatabaseDependency: TypeAlias = Callable[..., object]
IntrospectionServiceResolver: TypeAlias = Callable[
    [Request], RFC7662IntrospectionService
]
CallerAuthorizer: TypeAlias = Callable[
    [Request, Mapping[str, object], object], None | Awaitable[None]
]
TransportPolicy: TypeAlias = Callable[[Request], None]


async def _request_form_data(request: Request) -> dict[str, object]:
    form = getattr(request, "form", None)
    if callable(form):
        result = form()
        if inspect.isawaitable(result):
            result = await result
        if isinstance(result, Mapping):
            return dict(result)
        try:
            return {key: result.get(key) for key in result.keys()}
        except (AttributeError, TypeError):
            pass

    body = getattr(request, "body", b"") or b""
    if callable(body):
        result = body()
        body = await result if inspect.isawaitable(result) else result
    if isinstance(body, str):
        body = body.encode("utf-8")
    if not isinstance(body, (bytes, bytearray)):
        body = b""
    return {
        key: values[-1] if values else ""
        for key, values in parse_qs(
            bytes(body).decode("utf-8"), keep_blank_values=True
        ).items()
    }


def build_introspection_router(
    *,
    service_for_request: IntrospectionServiceResolver,
    authorize_caller: CallerAuthorizer,
    require_transport: TransportPolicy,
    get_db: DatabaseDependency,
) -> TigrblRouter:
    """Build one HTTP router around injected semantic/runtime collaborators."""

    router = TigrblRouter()

    @router.route("/introspect", methods=["POST"], response_model=IntrospectOut)
    async def introspect(request: Request, db: object = Depends(get_db)):
        require_transport(request)
        form_data = await _request_form_data(request)
        token = str(form_data.get("token") or "").strip()
        if not token:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "token parameter required",
            )
        authorization = authorize_caller(request, form_data, db)
        if inspect.isawaitable(authorization):
            await authorization
        try:
            return await service_for_request(request).introspect(token)
        except IntrospectionDisabledError as exc:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                "introspection disabled",
            ) from exc

    return router


def include_introspection_endpoint(
    app: TigrblApp,
    router: TigrblRouter,
    *,
    enabled: bool = True,
) -> None:
    """Mount the carrier once when selected by runtime composition."""

    path = "/introspect"
    routes = getattr(getattr(app, "router", None), "routes", ())
    if enabled and not any(
        (getattr(route, "path", None) or getattr(route, "path_template", None))
        == path
        for route in routes
    ):
        app.include_router(router)


__all__ = [
    "CallerAuthorizer",
    "DatabaseDependency",
    "IntrospectionServiceResolver",
    "TransportPolicy",
    "build_introspection_router",
    "include_introspection_endpoint",
]
