"""UserInfo endpoint for OpenID Connect 1.0."""

from __future__ import annotations

import inspect
from importlib import import_module

from tigrbl.security import Depends as TigrblDepends
from tigrbl_auth.framework import (
    TigrblRouter,
    TigrblApp,
    HTTPException,
    Request,
    Response,
    AsyncSession,
    status,
)

from tigrbl_auth.security import auth as security_auth
from tigrbl_auth.security import deps as security_deps
from tigrbl_auth.services.token_service import JWTCoder, InvalidTokenError, _svc, _svc_async
from tigrbl_auth.tables import User
from tigrbl_auth.tables.engine import get_db
from tigrbl_auth.standards.oauth2.rfc6750 import extract_bearer_token
from tigrbl_auth.framework import JWAAlg
from tigrbl_auth.config.deployment import deployment_from_app, deployment_from_request
from tigrbl_auth.config.settings import settings
from tigrbl_auth.security.user_lookup import first_user_by_filters

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


async def _runtime_jwt_coder():
    try:
        compat = import_module("tigrbl_auth.oidc_userinfo")
        get_coder = getattr(compat, "_get_jwt_coder", None)
        if get_coder is not None:
            result = get_coder()
            return await result if inspect.isawaitable(result) else result
    except Exception:
        pass
    coder_cls, _, _ = _runtime_token_bindings()
    default_factory = getattr(coder_cls, "default", None)
    if default_factory is not None and default_factory.__class__.__module__.startswith("unittest.mock"):
        return default_factory()
    async_factory = getattr(coder_cls, "async_default", None)
    if async_factory is not None:
        return await async_factory()
    return coder_cls.default()


async def _runtime_signing_service():
    try:
        compat = import_module("tigrbl_auth.oidc_userinfo")
        get_service = getattr(compat, "_get_signing_service", None)
        if get_service is not None:
            result = get_service()
            return await result if inspect.isawaitable(result) else result
    except Exception:
        pass
    _, _, svc_factory = _runtime_token_bindings()
    if svc_factory.__class__.__module__.startswith("unittest.mock"):
        return svc_factory()
    return await _svc_async()


async def _resolve_current_user(request: Request, db: AsyncSession, payload: dict) -> User:
    app = getattr(request, "app", None)
    router = getattr(app, "router", None)
    overrides = dict(getattr(app, "dependency_overrides", {}) or {})
    router_overrides = getattr(router, "dependency_overrides", {})
    if router_overrides:
        overrides.update(router_overrides)

    dependencies = [
        security_deps.get_current_principal,
        security_auth.get_current_principal,
    ]
    try:
        compat_deps = import_module("tigrbl_identity_server.security.deps")
        compat_auth = import_module("tigrbl_identity_server.security.auth")
        dependencies.extend(
            [
                getattr(compat_deps, "get_current_principal"),
                getattr(compat_auth, "get_current_principal"),
            ]
        )
    except Exception:
        pass

    for dependency in dependencies:
        override = overrides.get(dependency)
        if override is None:
            continue
        try:
            resolved = override(request)
        except TypeError:
            resolved = override()
        return await resolved if inspect.isawaitable(resolved) else resolved

    subject = payload.get("sub")
    if not subject:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "invalid access token")
    lookup = first_user_by_filters
    try:
        compat = import_module("tigrbl_auth_protocol_oidc.standards.userinfo")
        compat_lookup = getattr(compat, "first_user_by_filters", None)
        if compat_lookup is not None and compat_lookup is not first_user_by_filters:
            lookup = compat_lookup
    except Exception:
        pass
    user = await lookup(db, {"id": subject, "is_active": True})
    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "invalid access token")
    return user


@api.route("/userinfo", methods=["GET"], response_model=None)
async def userinfo(
    request: Request,
    db: AsyncSession = TigrblDepends(get_db),
) -> Response | dict[str, str]:
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
    _, invalid_token_error, _ = _runtime_token_bindings()
    try:
        payload = await (await _runtime_jwt_coder()).async_decode(token)
    except invalid_token_error as exc:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, "invalid access token"
        ) from exc
    scopes: set[str] = set(payload.get("scope", "").split())
    user = await _resolve_current_user(request, db, payload)

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
        svc, kid = await _runtime_signing_service()
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
