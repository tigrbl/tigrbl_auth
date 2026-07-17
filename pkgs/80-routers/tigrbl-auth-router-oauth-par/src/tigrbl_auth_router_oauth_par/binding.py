"""HTTP carrier binding for RFC 9126 pushed authorization requests."""

from __future__ import annotations

import inspect
import json
from collections.abc import Awaitable, Callable, Mapping
from typing import TypeAlias
from urllib.parse import parse_qs

from tigrbl import Depends, Request, TigrblApp, TigrblRouter
from tigrbl.runtime.status import HTTPException, status
from tigrbl_auth_protocol_oauth.schemas import PushedAuthorizationResponse
from tigrbl_auth_protocol_oauth.standards.pushed_authorization_requests import (
    PushedAuthorizationDisabledError,
    RFC9126PushedAuthorizationService,
)
from tigrbl_identity_contracts.oauth import (
    PushedAuthorizationPersistenceRequest,
)


DatabaseDependency: TypeAlias = Callable[..., object]
PushedAuthorizationServiceResolver: TypeAlias = Callable[
    [Request, object], RFC9126PushedAuthorizationService
]
PushedAuthorizationNormalizer: TypeAlias = Callable[
    [Request, Mapping[str, object]],
    Mapping[str, object] | Awaitable[Mapping[str, object]],
]
PushedAuthorizationAuthorizer: TypeAlias = Callable[
    [Request, Mapping[str, object], object],
    PushedAuthorizationPersistenceRequest
    | Awaitable[PushedAuthorizationPersistenceRequest],
]
PushedAuthorizationObserver: TypeAlias = Callable[
    [Request, Mapping[str, object]], None | Awaitable[None]
]


async def request_body_data(request: Request) -> dict[str, object]:
    """Decode a JSON or form-encoded request body without applying OAuth rules."""

    body = getattr(request, "body", b"") or b""
    if callable(body):
        value = body()
        body = await value if inspect.isawaitable(value) else value
    if isinstance(body, str):
        body = body.encode("utf-8")
    if not isinstance(body, (bytes, bytearray)):
        body = b""
    text = bytes(body).decode("utf-8")
    if not text:
        return {}
    try:
        payload = json.loads(text)
    except (TypeError, ValueError, json.JSONDecodeError):
        payload = None
    if isinstance(payload, Mapping):
        return dict(payload)
    return {
        key: values[-1] if len(values) == 1 else list(values)
        for key, values in parse_qs(text, keep_blank_values=True).items()
    }


async def _await_if_needed(value):
    return await value if inspect.isawaitable(value) else value


def build_pushed_authorization_router(
    *,
    service_for_request: PushedAuthorizationServiceResolver,
    normalize_request: PushedAuthorizationNormalizer,
    authorize_caller: PushedAuthorizationAuthorizer,
    observe_response: PushedAuthorizationObserver | None,
    get_db: DatabaseDependency,
) -> TigrblRouter:
    """Build the RFC 9126 carrier around injected runtime collaborators."""

    router = TigrblRouter()

    @router.route(
        "/par",
        methods=["POST"],
        response_model=PushedAuthorizationResponse,
    )
    async def pushed_authorization(request: Request, db=Depends(get_db)):
        service = service_for_request(request, db)
        if not service.enabled:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "PAR disabled")
        params = await request_body_data(request)
        normalized = await _await_if_needed(normalize_request(request, params))
        authorized = await _await_if_needed(
            authorize_caller(request, normalized, db)
        )
        if not isinstance(authorized, PushedAuthorizationPersistenceRequest):
            raise TypeError(
                "PAR authorizer must return PushedAuthorizationPersistenceRequest"
            )
        try:
            result = await service.push(
                client_id=authorized.client_id,
                tenant_id=authorized.tenant_id,
                params=authorized.params,
            )
        except PushedAuthorizationDisabledError as exc:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "PAR disabled") from exc
        payload: dict[str, object] = {
            "request_uri": result.request_uri,
            "expires_in": result.expires_in,
        }
        if observe_response is not None:
            await _await_if_needed(observe_response(request, payload))
        return payload

    return router


def include_pushed_authorization_endpoint(
    app: TigrblApp,
    router: TigrblRouter,
    *,
    enabled: bool = True,
) -> None:
    """Mount the RFC 9126 carrier once when selected by composition."""

    routes = getattr(getattr(app, "router", None), "routes", ())
    if enabled and not any(
        (getattr(route, "path", None) or getattr(route, "path_template", None))
        == "/par"
        for route in routes
    ):
        app.include_router(router)


__all__ = [
    "DatabaseDependency",
    "PushedAuthorizationAuthorizer",
    "PushedAuthorizationNormalizer",
    "PushedAuthorizationObserver",
    "PushedAuthorizationServiceResolver",
    "build_pushed_authorization_router",
    "include_pushed_authorization_endpoint",
    "request_body_data",
]
