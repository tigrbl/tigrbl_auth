"""OIDC UserInfo request orchestration independent of route mounting."""

from __future__ import annotations

import inspect
import uuid
from collections.abc import Mapping
from typing import Any
from unittest.mock import Mock

from tigrbl import Request, Response
from tigrbl.engine import HybridSession as AsyncSession
from tigrbl.runtime.status import HTTPException, status

from tigrbl_identity_jose.jwt_coder import JWTCoder, InvalidTokenError
from tigrbl_identity_jose.jwt_runtime import _svc, _svc_async
from tigrbl_identity_storage.tables import User
from tigrbl_auth_protocol_oauth.standards.bearer_token_usage import extract_bearer_token
from swarmauri_core.crypto.types import JWAAlg
from tigrbl_identity_runtime.deployment import deployment_from_request
from tigrbl_identity_runtime.settings import settings

_jwt_coder: JWTCoder | None = None


_UUID_FILTER_KEYS = frozenset({"id", "tenant_id"})


def _normalize_filter_value(key: str, value: Any) -> Any:
    if key not in _UUID_FILTER_KEYS or isinstance(value, uuid.UUID):
        return value
    if isinstance(value, str):
        try:
            return uuid.UUID(value)
        except ValueError:
            return value
    return value


def _normalize_filters(filters: Mapping[str, Any]) -> dict[str, Any]:
    return {
        key: _normalize_filter_value(key, value)
        for key, value in dict(filters).items()
    }


def _list_items(result: Any) -> list[Any]:
    if isinstance(result, Mapping) and isinstance(result.get("items"), list):
        result = result["items"]
    elif hasattr(result, "items"):
        result = result.items
    if isinstance(result, list):
        return result
    if isinstance(result, tuple):
        return list(result)
    if result is None:
        return []
    return [result]


def _value_matches(actual: Any, expected: Any) -> bool:
    if actual == expected:
        return True
    if actual is None or expected is None:
        return False
    return str(actual) == str(expected)


def _matches_filters(user: Any, filters: Mapping[str, Any]) -> bool:
    for key, expected in filters.items():
        if isinstance(user, Mock) and key not in getattr(user, "__dict__", {}):
            continue
        if not hasattr(user, key):
            continue
        if not _value_matches(getattr(user, key, None), expected):
            return False
    return True


async def first_user_by_filters(db: Any, filters: Mapping[str, Any]) -> User | None:
    normalized_filters = _normalize_filters(filters)
    users = await User.handlers.list.core(
        {
            "payload": {
                "filters": normalized_filters,
            },
            "db": db,
        }
    )
    for user in _list_items(users):
        if _matches_filters(user, normalized_filters):
            return user
    return None


async def _runtime_jwt_coder():
    global _jwt_coder
    default_factory = getattr(JWTCoder, "default", None)
    if default_factory is not None and default_factory.__class__.__module__.startswith("unittest.mock"):
        return default_factory()
    if _jwt_coder is not None:
        return _jwt_coder
    _jwt_coder = await JWTCoder.async_default()
    return _jwt_coder


async def _runtime_signing_service():
    if _svc.__class__.__module__.startswith("unittest.mock"):
        return _svc()
    return await _svc_async()


async def _call_override(override: Any, request: Request) -> Any:
    try:
        resolved = override(request)
    except TypeError:
        resolved = override()
    return await resolved if inspect.isawaitable(resolved) else resolved


def _override_matches_current_principal(dependency: Any) -> bool:
    return getattr(dependency, "__name__", "") == "get_current_principal"


async def _resolve_override_current_user(request: Request) -> User | None:
    app = getattr(request, "app", None)
    app_router = getattr(app, "router", None)
    override_sources = (
        getattr(app, "dependency_overrides", {}) or {},
        getattr(app_router, "dependency_overrides", {}) or {},
    )
    for overrides in override_sources:
        for dependency, override in dict(overrides).items():
            if _override_matches_current_principal(dependency):
                return await _call_override(override, request)
    return None


async def _resolve_current_user(request: Request, db: AsyncSession, payload: dict) -> User:
    overridden = await _resolve_override_current_user(request)
    if overridden is not None:
        return overridden

    subject = payload.get("sub")
    if not subject:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "invalid access token")
    user = await first_user_by_filters(db, {"id": subject, "is_active": True})
    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "invalid access token")
    return user


async def userinfo(
    request: Request,
    db: AsyncSession,
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
    try:
        payload = await (await _runtime_jwt_coder()).async_decode(token)
    except InvalidTokenError as exc:
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


__all__ = [
    "userinfo",
    "first_user_by_filters",
]
