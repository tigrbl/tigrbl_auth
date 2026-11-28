"""HTTP carrier binding for the OAuth/OIDC authorization endpoint."""

from __future__ import annotations

from collections.abc import Awaitable, Callable, Mapping
from typing import Any, TypeAlias
from urllib.parse import parse_qs

from tigrbl import Depends, Request, TigrblApp, TigrblRouter


DatabaseDependency: TypeAlias = Callable[..., object]
AuthorizationRequestTarget: TypeAlias = Callable[
    ...,
    Any | Awaitable[Any],
]


def _request_params(
    request: Request,
    *,
    response_type: str | None,
    client_id: str | None,
    redirect_uri: str | None,
    scope: str | None,
    response_mode: str | None,
    state: str | None,
    nonce: str | None,
    code_challenge: str | None,
    code_challenge_method: str | None,
    prompt: str | None,
    max_age: int | None,
    login_hint: str | None,
    claims: str | None,
    request_uri: str | None,
    request_object: str | None,
    authorization_details: str | None,
) -> Mapping[str, object | None]:
    query = request.query_params
    if hasattr(query, "getlist"):
        resources = list(query.getlist("resource"))
    elif hasattr(query, "get_all"):
        resources = list(query.get_all("resource"))
    else:
        raw_query = getattr(request, "scope", {}).get("query_string", b"")
        if isinstance(raw_query, bytes):
            raw_query = raw_query.decode("utf-8")
        if not raw_query:
            raw_query = str(getattr(request.url, "query", ""))
        resources = parse_qs(
            str(raw_query),
            keep_blank_values=True,
        ).get("resource")
    return {
        "response_type": response_type or query.get("response_type"),
        "client_id": client_id or query.get("client_id"),
        "redirect_uri": redirect_uri or query.get("redirect_uri"),
        "scope": scope or query.get("scope"),
        "response_mode": response_mode or query.get("response_mode"),
        "state": state or query.get("state"),
        "nonce": nonce or query.get("nonce"),
        "code_challenge": code_challenge or query.get("code_challenge"),
        "code_challenge_method": (
            code_challenge_method or query.get("code_challenge_method")
        ),
        "prompt": prompt or query.get("prompt"),
        "max_age": max_age if max_age is not None else query.get("max_age"),
        "login_hint": login_hint or query.get("login_hint"),
        "claims": claims or query.get("claims"),
        "request_uri": request_uri or query.get("request_uri"),
        "request": request_object or query.get("request"),
        "authorization_details": (
            authorization_details or query.get("authorization_details")
        ),
        "resource": resources,
    }


def build_authorization_router(
    *,
    authorize_request: AuthorizationRequestTarget,
    get_db: DatabaseDependency,
) -> TigrblRouter:
    """Build the GET carrier around injected authorization orchestration."""

    router = TigrblRouter()

    @router.route("/authorize", methods=["GET"])
    async def authorize(
        request: Request,
        response_type: str | None = None,
        client_id: str | None = None,
        redirect_uri: str | None = None,
        scope: str | None = None,
        response_mode: str | None = None,
        state: str | None = None,
        nonce: str | None = None,
        code_challenge: str | None = None,
        code_challenge_method: str | None = None,
        prompt: str | None = None,
        max_age: int | None = None,
        login_hint: str | None = None,
        claims: str | None = None,
        request_uri: str | None = None,
        request_object: str | None = None,
        authorization_details: str | None = None,
        db: object = Depends(get_db),
    ) -> Any:
        params = _request_params(
            request,
            response_type=response_type,
            client_id=client_id,
            redirect_uri=redirect_uri,
            scope=scope,
            response_mode=response_mode,
            state=state,
            nonce=nonce,
            code_challenge=code_challenge,
            code_challenge_method=code_challenge_method,
            prompt=prompt,
            max_age=max_age,
            login_hint=login_hint,
            claims=claims,
            request_uri=request_uri,
            request_object=request_object,
            authorization_details=authorization_details,
        )
        return await authorize_request(request=request, db=db, params=dict(params))

    return router


def include_authorization_endpoint(
    app: TigrblApp,
    router: TigrblRouter,
    *,
    enabled: bool = True,
) -> None:
    """Mount the authorization carrier once when selected by composition."""

    routes = getattr(getattr(app, "router", None), "routes", ())
    if enabled and not any(
        (getattr(route, "path", None) or getattr(route, "path_template", None))
        == "/authorize"
        for route in routes
    ):
        app.include_router(router)


__all__ = [
    "AuthorizationRequestTarget",
    "DatabaseDependency",
    "build_authorization_router",
    "include_authorization_endpoint",
]
