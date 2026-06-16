from __future__ import annotations

import inspect
from typing import Any, Callable
from uuid import UUID

from tigrbl_auth.framework import HTTPException, Request, status

from tigrbl_auth.services.token_service import JWTCoder
from tigrbl_auth.services.auth_backends import PasswordBackend
from tigrbl_auth.config.settings import settings
from tigrbl_auth.config.deployment import ResolvedDeployment, resolve_deployment
from tigrbl_auth.standards.oidc.frontchannel_logout import mark_frontchannel_complete
from tigrbl_auth.standards.oidc.backchannel_logout import mark_backchannel_complete
from tigrbl_auth.standards.oauth2.rfc9700 import runtime_security_profile


class _LazyRuntimeProxy:
    """Resolve heavyweight runtime helpers on first attribute access.

    This keeps module import side effects out of the public REST helper surface,
    which avoids circular imports during clean-room app materialization while
    preserving the historical object-shaped API expected by callers.
    """

    __slots__ = ("_factory", "_value")

    def __init__(self, factory: Callable[[], Any]):
        object.__setattr__(self, "_factory", factory)
        object.__setattr__(self, "_value", None)

    def _resolve(self) -> Any:
        if self._value is None:
            self._value = self._factory()
        return self._value

    async def _resolve_async(self) -> Any:
        if self._value is not None:
            return self._value
        owner = getattr(self._factory, "__self__", None)
        async_factory = getattr(owner, "async_default", None)
        if callable(async_factory):
            self._value = await async_factory()
            return self._value
        value = self._factory()
        if inspect.isawaitable(value):
            value = await value
        self._value = value
        return self._value

    def __getattr__(self, name: str) -> Any:
        if name.startswith("async_"):
            async def _async_method(*args: Any, **kwargs: Any) -> Any:
                target = await self._resolve_async()
                method = getattr(target, name)
                result = method(*args, **kwargs)
                return await result if inspect.isawaitable(result) else result

            return _async_method
        return getattr(self._resolve(), name)

    def __setattr__(self, name: str, value: Any) -> None:
        if name in {"_factory", "_value"}:
            object.__setattr__(self, name, value)
            return
        setattr(self._resolve(), name, value)

    def __delattr__(self, name: str) -> None:
        if name in {"_factory", "_value"}:
            object.__delattr__(self, name)
            return
        delattr(self._resolve(), name)

    def __repr__(self) -> str:  # pragma: no cover - debugging helper
        return repr(self._resolve())


_jwt = _LazyRuntimeProxy(JWTCoder.default)
_pwd_backend = _LazyRuntimeProxy(PasswordBackend)

_ALLOWED_GRANT_TYPES = {"password", "authorization_code", "client_credentials", "refresh_token"}
if settings.enable_rfc8628:
    _ALLOWED_GRANT_TYPES.add("urn:ietf:params:oauth:grant-type:device_code")


def allowed_grant_types(settings_obj: object | None = None) -> set[str]:
    deployment = resolve_deployment(settings_obj or settings)
    policy = runtime_security_profile(deployment)
    return set(policy.allowed_grant_types)


def _require_tls(request: Request, deployment: ResolvedDeployment | None = None) -> None:
    scope = getattr(request, "scope", {})
    scheme = scope.get("scheme") if isinstance(scope, dict) else None
    if not scheme:
        try:
            url = request.url
            scheme = url.scheme if hasattr(url, "scheme") else str(url).split(":", 1)[0]
        except Exception:
            scheme = "http"
    active_deployment = deployment or resolve_deployment(settings)
    if active_deployment.flag_enabled("require_tls") and scheme != "https":
        raise HTTPException(status.HTTP_400_BAD_REQUEST, {"error": "tls_required"})


async def _front_channel_logout(logout_id: str) -> None:
    try:
        await mark_frontchannel_complete(UUID(logout_id))
    except Exception:
        return None


async def _back_channel_logout(logout_id: str) -> None:
    try:
        await mark_backchannel_complete(UUID(logout_id))
    except Exception:
        return None
