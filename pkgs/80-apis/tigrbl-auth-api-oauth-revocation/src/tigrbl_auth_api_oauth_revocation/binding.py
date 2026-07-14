"""HTTP carrier binding for RFC 7009 token revocation."""

from __future__ import annotations

import inspect
from collections.abc import Callable, Mapping
from typing import TypeAlias
from urllib.parse import parse_qs

from tigrbl import Request, TigrblApp, TigrblRouter
from tigrbl.runtime.status import HTTPException, status
from tigrbl_auth_protocol_oauth.schemas import RevocationOut
from tigrbl_auth_protocol_oauth.standards.revocation import (
    CANONICAL_REVOCATION_PATH,
    RFC7009RevocationService,
    RevocationDisabledError,
)


RevocationServiceResolver: TypeAlias = Callable[
    [Request], RFC7009RevocationService
]


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


def build_revocation_router(
    *,
    service_for_request: RevocationServiceResolver,
) -> TigrblRouter:
    router = TigrblRouter()

    @router.route(
        CANONICAL_REVOCATION_PATH,
        methods=["POST"],
        response_model=RevocationOut,
    )
    async def revoke(request: Request) -> dict[str, bool]:
        form_data = await _request_form_data(request)
        token = str(form_data.get("token") or "").strip()
        if not token:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "token parameter required",
            )
        token_type_hint = str(form_data.get("token_type_hint") or "").strip()
        try:
            await service_for_request(request).revoke(
                token,
                token_type_hint=token_type_hint or None,
            )
        except RevocationDisabledError as exc:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                "revocation disabled",
            ) from exc
        return {"revoked": True}

    return router


def include_revocation_endpoint(
    app: TigrblApp,
    router: TigrblRouter,
    *,
    enabled: bool = True,
) -> None:
    if enabled and not any(
        (getattr(route, "path", None) or getattr(route, "path_template", None))
        == CANONICAL_REVOCATION_PATH
        for route in app.router.routes
    ):
        app.include_router(router)


__all__ = [
    "RevocationServiceResolver",
    "build_revocation_router",
    "include_revocation_endpoint",
]
