"""UserInfo endpoint for OpenID Connect 1.0."""

from __future__ import annotations

import inspect
from importlib import import_module

from tigrbl_auth.framework import (
    TigrblRouter,
    TigrblApp,
    HTTPException,
    Request,
    Response,
    status,
)

from tigrbl_auth.security import auth as security_auth
from tigrbl_auth.security import deps as security_deps
from tigrbl_auth.services.token_service import JWTCoder, InvalidTokenError, _svc
from tigrbl_auth.tables import User
from tigrbl_auth.standards.oauth2.rfc6750 import extract_bearer_token
from tigrbl_auth.framework import JWAAlg
from tigrbl_auth.config.deployment import deployment_from_app, deployment_from_request
from tigrbl_auth.config.settings import settings

api = TigrblRouter()
router = api


def _runtime_token_bindings():
    try:
        compat = import_module("tigrbl_auth.oidc_userinfo")
    except Exception:
        return JWTCoder, InvalidTokenError, _svc
    return (
        getattr(compat, "JWTCoder", JWTCoder),
        getattr(compat, "InvalidTokenError", InvalidTokenError),
        getattr(compat, "_svc", _svc),
    )


async def _resolve_current_user(request: Request) -> User:
    app = getattr(request, "app", None)
    router = getattr(app, "router", None)
    overrides = dict(getattr(app, "dependency_overrides", {}) or {})
    router_overrides = getattr(router, "dependency_overrides", {})
    if router_overrides:
        overrides.update(router_overrides)

    for dependency in (
        security_deps.get_current_principal,
        security_auth.get_current_principal,
    ):
        override = overrides.get(dependency)
        if override is None:
            continue
        try:
            resolved = override(request)
        except TypeError:
            resolved = override()
        return await resolved if inspect.isawaitable(resolved) else resolved

    return await security_deps.get_current_principal(request)


@api.route("/userinfo", methods=["GET"], response_model=None)
async def userinfo(request: Request) -> Response | dict[str, str]:
    deployment = deployment_from_request(request, settings)
    if not deployment.route_enabled("/userinfo"):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "OIDC UserInfo disabled")

    token = await extract_bearer_token(
        request,
        request.headers.get("Authorization")
        or request.headers.get("authorization", ""),
    )
    if not token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "missing access token")
    coder_cls, invalid_token_error, svc_factory = _runtime_token_bindings()
    try:
        payload = await coder_cls.default().async_decode(token)
    except invalid_token_error as exc:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, "invalid access token"
        ) from exc
    scopes: set[str] = set(payload.get("scope", "").split())
    user = await _resolve_current_user(request)

    claims: dict[str, str] = {"sub": str(user.id)}
    if "profile" in scopes:
        claims["name"] = user.username
    if "email" in scopes:
        claims["email"] = user.email
    if "address" in scopes and getattr(user, "address", None):
        claims["address"] = getattr(user, "address")
    if "phone" in scopes and getattr(user, "phone", None):
        claims["phone_number"] = getattr(user, "phone")

    if "application/jwt" in (
        request.headers.get("Accept") or request.headers.get("accept", "")
    ):
        svc, kid = svc_factory()
        token = await svc.mint(claims, alg=JWAAlg.EDDSA, kid=kid)
        return Response(body=str(token).encode("utf-8"), headers={"content-type": "application/jwt"}, media_type="application/jwt")

    return claims


def include_oidc_userinfo(app: TigrblApp) -> None:
    deployment = deployment_from_app(app, settings)
    if not deployment.route_enabled("/userinfo"):
        return
    if not any(
        (getattr(route, "path", None) or getattr(route, "path_template", None))
        == "/userinfo"
        for route in app.router.routes
    ):
        app.include_router(api)


__all__ = ["api", "router", "include_oidc_userinfo"]
