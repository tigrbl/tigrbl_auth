"""Domain-organized OAuth 2.0 token introspection support.

The canonical implementation uses durable persistence and the Tigrbl runtime.
When those dependencies are not importable, a dependency-light checkpoint
fallback is used so standards helpers, docs generation, and targeted tests can
still execute.
"""

from __future__ import annotations

from http import HTTPStatus as _HTTPStatus
import base64
import inspect
from typing import Any, Dict, Final
from urllib.parse import parse_qs

from tigrbl_identity_runtime.settings import settings

try:  # pragma: no cover - exercised when the full runtime stack is installed
    from tigrbl_identity_contracts.rest import IntrospectOut
    from tigrbl_identity_server.rest.shared import _require_tls
    from tigrbl_identity_runtime.deployment import deployment_from_request
    from tigrbl_identity_server.framework import HTTPException, Request, TigrblApp, TigrblRouter, status
    from tigrbl_identity_server.framework import AsyncSession, Depends
    from tigrbl_auth_protocol_oauth.ops.token import _load_client, _registered_token_endpoint_auth_method
    from tigrbl_identity_storage.persistence import (
        introspect_token_async as _introspect_token_async,
        introspect_token as _introspect_token,
        record_token as _record_token,
        reset_token_state_async as _reset_token_state_async,
        reset_token_state as _reset_token_state,
        unregister_token as _unregister_token,
        upsert_token_record_async as _record_token_async,
    )
    from tigrbl_auth_protocol_oauth.standards.jwt_client_auth import (
        PRIVATE_KEY_JWT_AUTH_METHOD,
        authenticate_client_assertion,
    )
    from tigrbl_auth_protocol_oauth.standards.mtls import (
        SUPPORTED_MTLS_AUTH_METHODS,
        authenticate_mtls_client,
        presented_certificate_thumbprint,
    )
    from tigrbl_identity_storage.tables.engine import get_db
except Exception:  # pragma: no cover - dependency-light checkpoint fallback
    IntrospectOut = dict  # type: ignore[assignment]
    AsyncSession = Any  # type: ignore[assignment]

    def Depends(dep: Any) -> Any:  # type: ignore[misc]
        return dep

    def get_db() -> Any:
        return None

    def _require_tls(_request: Any) -> None:
        return None

    def deployment_from_request(_request: Any, _fallback_settings: object | None = None) -> Any:
        return None

    async def _load_client(_db: Any, _client_id: str) -> tuple[Any, Any]:
        return None, None

    def _registered_token_endpoint_auth_method(_registration: Any) -> str:
        return "client_secret_basic"

    PRIVATE_KEY_JWT_AUTH_METHOD = "private_key_jwt"
    SUPPORTED_MTLS_AUTH_METHODS = ("tls_client_auth", "self_signed_tls_client_auth")

    def authenticate_client_assertion(**_kwargs: Any) -> dict[str, object]:
        raise ValueError("unsupported client_assertion_type")

    def authenticate_mtls_client(*_args: Any, **_kwargs: Any) -> Any:
        raise ValueError("client certificate thumbprint required for mTLS client authentication")

    def presented_certificate_thumbprint(_request: Any) -> str | None:
        return None

    class HTTPException(Exception):
        def __init__(self, status_code: int, detail: str):
            super().__init__(detail)
            self.status_code = status_code
            self.detail = detail

    class _Status:
        HTTP_404_NOT_FOUND = int(_HTTPStatus.NOT_FOUND)
        HTTP_400_BAD_REQUEST = int(_HTTPStatus.BAD_REQUEST)

    status = _Status()

    class Request:  # pragma: no cover - typing/documentation stub
        body: bytes = b""

    class _Route:
        def __init__(self, path: str):
            self.path = path
            self.path_template = path

    class TigrblRouter:
        def __init__(self):
            self.routes: list[_Route] = []

        def route(self, path: str, **_kwargs: Any):
            def _decorator(func):
                self.routes.append(_Route(path))
                return func

            return _decorator

    class TigrblApp:  # pragma: no cover - fallback stub
        def __init__(self):
            self.router = TigrblRouter()

        def include_router(self, router: TigrblRouter) -> None:
            existing = {
                getattr(route, "path", None) or getattr(route, "path_template", None)
                for route in self.router.routes
            }
            for route in router.routes:
                path = getattr(route, "path", None) or getattr(route, "path_template", None)
                if path not in existing:
                    self.router.routes.append(route)

    _TOKENS: dict[str, dict[str, Any]] = {}

    def _record_token(token: str, claims: Dict[str, Any], token_kind: str | None = None) -> str:
        payload = dict(claims)
        if token_kind is not None and "kind" not in payload:
            payload["kind"] = token_kind
        _TOKENS[token] = payload
        return token

    def _unregister_token(token: str) -> None:
        _TOKENS.pop(token, None)

    def _introspect_token(token: str) -> Dict[str, Any]:
        claims = _TOKENS.get(token)
        if claims is None:
            return {"active": False}
        return {"active": True, **claims}

    async def _introspect_token_async(token: str) -> Dict[str, Any]:
        return _introspect_token(token)

    async def _record_token_async(token: str, claims: Dict[str, Any], token_kind: str | None = None) -> str:
        return _record_token(token, claims, token_kind=token_kind)

    def _reset_token_state() -> None:
        _TOKENS.clear()

    async def _reset_token_state_async() -> None:
        _reset_token_state()

RFC7662_SPEC_URL: Final[str] = "https://www.rfc-editor.org/rfc/rfc7662"

api = TigrblRouter()
router = api
_FALLBACK_TOKENS: dict[str, dict[str, Any]] = {}


def _protected_resource_verifier_contract(request: Any):
    from tigrbl_auth_protocol_oauth.standards.resource_verifier_contract import protected_resource_verifier_contract_from_request

    return protected_resource_verifier_contract_from_request(request)


def _header(request: Any, name: str) -> str | None:
    headers = getattr(request, "headers", {}) or {}
    if hasattr(headers, "get"):
        return headers.get(name) or headers.get(name.lower())
    return None


def _introspection_endpoint_audiences(request: Any) -> set[str]:
    deployment = deployment_from_request(request, settings)
    issuer = str(getattr(deployment, "issuer", None) or settings.issuer).rstrip("/")
    audiences = {
        issuer,
        f"{issuer}/introspect",
        f"{issuer}/token",
    }
    return {value for value in audiences if value}


async def _authorize_introspection_caller(
    request: Any,
    form_data: dict[str, Any],
    db: AsyncSession,
) -> None:
    verifier_contract = _protected_resource_verifier_contract(request)
    allowed_auth_methods = set(verifier_contract.introspection_auth_methods)
    auth = _header(request, "Authorization") or ""
    client_assertion = str(form_data.get("client_assertion") or "").strip()
    client_assertion_type = str(form_data.get("client_assertion_type") or "").strip()
    client_id = None
    client_secret = None

    if auth.startswith("Basic "):
        try:
            decoded = base64.b64decode(auth.split()[1]).decode()
            client_id, client_secret = decoded.split(":", 1)
        except Exception as exc:
            raise HTTPException(int(_HTTPStatus.UNAUTHORIZED), "invalid_client") from exc
    else:
        client_id = str(form_data.get("client_id") or "").strip() or None
        client_secret = str(form_data.get("client_secret") or "").strip() or None

    if not client_id and not client_assertion:
        raise HTTPException(int(_HTTPStatus.UNAUTHORIZED), "authenticated caller required")

    if client_assertion and not client_id:
        try:
            claims = authenticate_client_assertion(
                client_assertion_type=client_assertion_type,
                client_assertion=client_assertion,
                audience=_introspection_endpoint_audiences(request),
                client_id=None,
            )
        except ValueError as exc:
            raise HTTPException(int(_HTTPStatus.UNAUTHORIZED), "invalid_client") from exc
        client_id = str(claims.get("iss") or "").strip() or None

    if not client_id:
        raise HTTPException(int(_HTTPStatus.UNAUTHORIZED), "authenticated caller required")

    client, registration = await _load_client(db, str(client_id))
    if client is None:
        raise HTTPException(int(_HTTPStatus.UNAUTHORIZED), "invalid_client")

    registered_auth_method = _registered_token_endpoint_auth_method(registration)
    raw_registration_metadata = getattr(registration, "registration_metadata", None) if registration is not None else None
    registration_metadata = dict(raw_registration_metadata) if isinstance(raw_registration_metadata, dict) else {}

    if client_assertion:
        if PRIVATE_KEY_JWT_AUTH_METHOD not in allowed_auth_methods:
            raise HTTPException(int(_HTTPStatus.UNAUTHORIZED), "invalid_client")
        if registered_auth_method != PRIVATE_KEY_JWT_AUTH_METHOD:
            raise HTTPException(int(_HTTPStatus.UNAUTHORIZED), "invalid_client")
        try:
            authenticate_client_assertion(
                client_assertion_type=client_assertion_type,
                client_assertion=client_assertion,
                audience=_introspection_endpoint_audiences(request),
                client_id=str(client.id),
                token_endpoint_auth_method=registered_auth_method,
            )
        except ValueError as exc:
            raise HTTPException(int(_HTTPStatus.UNAUTHORIZED), "invalid_client") from exc
        return None

    if registered_auth_method in SUPPORTED_MTLS_AUTH_METHODS:
        if registered_auth_method not in allowed_auth_methods:
            raise HTTPException(int(_HTTPStatus.UNAUTHORIZED), "invalid_client")
        try:
            authenticate_mtls_client(
                registration_metadata,
                presented_certificate_thumbprint(request),
                token_endpoint_auth_method=registered_auth_method,
            )
        except ValueError as exc:
            raise HTTPException(int(_HTTPStatus.UNAUTHORIZED), "invalid_client") from exc
        return None

    if registered_auth_method == "client_secret_post":
        if registered_auth_method not in allowed_auth_methods:
            raise HTTPException(int(_HTTPStatus.UNAUTHORIZED), "invalid_client")
        if not client_secret:
            raise HTTPException(int(_HTTPStatus.UNAUTHORIZED), "invalid_client")
    elif registered_auth_method == "client_secret_basic":
        if registered_auth_method not in allowed_auth_methods:
            raise HTTPException(int(_HTTPStatus.UNAUTHORIZED), "invalid_client")
        if not auth.startswith("Basic ") or not client_secret:
            raise HTTPException(int(_HTTPStatus.UNAUTHORIZED), "invalid_client")
    else:
        raise HTTPException(int(_HTTPStatus.UNAUTHORIZED), "invalid_client")

    secret_valid = client.verify_secret(client_secret)
    if inspect.isawaitable(secret_valid):
        secret_valid = await secret_valid
    if not secret_valid:
        raise HTTPException(int(_HTTPStatus.UNAUTHORIZED), "invalid_client")
    return None


def register_token(token: str, claims: Dict[str, Any] | None = None) -> str:
    payload = dict(claims or {})
    _FALLBACK_TOKENS[token] = payload
    return _record_token(token, payload, token_kind=payload.get("kind"))


async def register_token_async(token: str, claims: Dict[str, Any] | None = None) -> str:
    payload = dict(claims or {})
    _FALLBACK_TOKENS[token] = payload
    return await _record_token_async(token, payload, token_kind=payload.get("kind"))


async def _request_form_data(request: Request) -> dict[str, Any]:
    form = getattr(request, "form", None)
    if callable(form):
        result = form()
        if inspect.isawaitable(result):
            result = await result
        if isinstance(result, dict):
            return dict(result)
        try:
            return {key: result.get(key) for key in result.keys()}
        except Exception:
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
        key: values[-1] if isinstance(values, list) and values else values
        for key, values in parse_qs(bytes(body).decode("utf-8"), keep_blank_values=True).items()
    }


def unregister_token(token: str) -> None:
    _FALLBACK_TOKENS.pop(token, None)
    _unregister_token(token)


def introspect_token(token: str) -> Dict[str, Any]:
    if not settings.enable_rfc7662:
        raise RuntimeError(f"RFC 7662 support is disabled: {RFC7662_SPEC_URL}")
    payload = _introspect_token(token)
    if payload.get("active") is False and token in _FALLBACK_TOKENS:
        return {"active": True, **_FALLBACK_TOKENS[token]}
    return payload


async def introspect_token_async(token: str) -> Dict[str, Any]:
    if not settings.enable_rfc7662:
        raise RuntimeError(f"RFC 7662 support is disabled: {RFC7662_SPEC_URL}")
    payload = await _introspect_token_async(token)
    if payload.get("active") is False and token in _FALLBACK_TOKENS:
        return {"active": True, **_FALLBACK_TOKENS[token]}
    return payload


def reset_tokens() -> None:
    _FALLBACK_TOKENS.clear()
    _reset_token_state()


async def reset_tokens_async() -> None:
    _FALLBACK_TOKENS.clear()
    await _reset_token_state_async()


@api.route("/introspect", methods=["POST"], response_model=IntrospectOut)
async def introspect(request: Request, db: AsyncSession = Depends(get_db)):
    _require_tls(request, deployment=deployment_from_request(request, settings))
    if not settings.enable_rfc7662:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "introspection disabled")
    form_data = await _request_form_data(request)
    token_value = form_data.get("token")
    token = token_value[-1] if isinstance(token_value, list) and token_value else token_value
    if not token:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "token parameter required")
    await _authorize_introspection_caller(request, form_data, db)
    return await introspect_token_async(token)


def include_introspection_endpoint(app: TigrblApp) -> None:
    path = "/introspect"
    routes = getattr(getattr(app, "router", None), "routes", [])
    if settings.enable_rfc7662 and not any(
        (getattr(route, "path", None) or getattr(route, "path_template", None)) == path
        for route in routes
    ):
        app.include_router(api)


include_rfc7662 = include_introspection_endpoint


__all__ = [
    "RFC7662_SPEC_URL",
    "api",
    "router",
    "register_token",
    "register_token_async",
    "unregister_token",
    "introspect_token",
    "introspect_token_async",
    "reset_tokens",
    "reset_tokens_async",
    "introspect",
    "include_introspection_endpoint",
    "include_rfc7662",
]
