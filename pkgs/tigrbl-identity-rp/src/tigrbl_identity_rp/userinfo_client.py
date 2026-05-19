"""UserInfo endpoint for OpenID Connect 1.0.

This module implements the `/userinfo` endpoint as described in the
OpenID Connect Core specification.  It is **not** tied to an RFC so it
lives in the OIDC namespace instead of an `rfcXXXX` module.

The endpoint returns a set of claims about the authenticated user based
on the scopes granted to the access token.  Unrequested claim groups are
omitted from the response.
"""

from __future__ import annotations

import inspect

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

api = TigrblRouter()
router = api


async def _resolve_current_user(request: Request) -> User:
    """Resolve the current principal, honoring app/router dependency overrides."""

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
    """Return claims about the authenticated user.

    The caller must present a valid access token in the ``Authorization``
    header.  Returned claims are filtered based on scopes granted in that
    token.  If the request ``Accept`` header includes ``application/jwt`` the
    response will be JWS signed.
    """

    token = await extract_bearer_token(
        request,
        request.headers.get("Authorization")
        or request.headers.get("authorization", ""),
    )
    if not token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "missing access token")
    try:
        payload = await JWTCoder.default().async_decode(token)
    except InvalidTokenError as exc:
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
        svc, kid = _svc()
        token = await svc.mint(claims, alg=JWAAlg.EDDSA, kid=kid)
        return Response(body=str(token).encode("utf-8"), headers={"content-type": "application/jwt"}, media_type="application/jwt")

    return claims


# ---------------------------------------------------------------------------
# Tigrbl integration
# ---------------------------------------------------------------------------


def include_oidc_userinfo(app: TigrblApp) -> None:
    """Attach the UserInfo endpoint to *app* if not already present."""

    if not any(
        (getattr(route, "path", None) or getattr(route, "path_template", None))
        == "/userinfo"
        for route in app.router.routes
    ):
        app.include_router(api)


__all__ = ["api", "router", "include_oidc_userinfo"]
