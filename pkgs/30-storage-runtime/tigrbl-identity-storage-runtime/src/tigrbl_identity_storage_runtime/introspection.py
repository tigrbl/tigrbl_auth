"""RFC 7662 token introspection runtime publisher."""

from __future__ import annotations

from http import HTTPStatus as _HTTPStatus
import base64
import inspect
from typing import Any, Dict, Final
from urllib.parse import parse_qs
from uuid import UUID

from tigrbl_auth_protocol_oauth.standards._introspection_activity import (
    apply_introspection_activity_constraints as _apply_introspection_activity_constraints,
    header as _header,
)
from tigrbl_auth_protocol_oauth.standards.jwt_client_auth import (
    PRIVATE_KEY_JWT_AUTH_METHOD,
    authenticate_client_assertion,
)
from tigrbl_auth_protocol_oauth.standards.mutual_tls_client_authentication import (
    SUPPORTED_MTLS_AUTH_METHODS,
    authenticate_mtls_client,
    presented_certificate_pem,
    presented_certificate_thumbprint,
)
from tigrbl_auth_protocol_oauth.standards.resource_verifier_contract import (
    protected_resource_verifier_contract_from_request,
)
from tigrbl_identity_runtime.deployment import deployment_from_request
from tigrbl_identity_runtime.settings import settings
from tigrbl_identity_storage.framework import (
    AsyncSession,
    Depends,
    HTTPException,
    Request,
    TigrblApp,
    TigrblRouter,
    status,
)
from tigrbl_identity_storage.tables._ops import first_handler_record, read_handler_record
from tigrbl_identity_storage.tables._sync import run_async
from tigrbl_identity_storage.tables.client import Client
from tigrbl_identity_storage.tables.client_registration import ClientRegistration
from tigrbl_identity_storage.tables.engine import get_db
from tigrbl_identity_storage.tables.revoked_token._op import (
    reset_token_state as _reset_token_state,
    reset_token_state_async as _reset_token_state_async,
)
from tigrbl_identity_storage.tables.token_record import IntrospectOut
from tigrbl_identity_storage.tables.token_record._introspection_store import (
    introspect_token_record_async as _introspect_token_async,
)
from tigrbl_identity_storage.tables.token_record._lifecycle import (
    remove_token_record_async,
    upsert_token_record_async as _record_token_async,
)


RFC7662_SPEC_URL: Final[str] = "https://www.rfc-editor.org/rfc/rfc7662"
DEFAULT_TOKEN_ENDPOINT_AUTH_METHOD: Final[str] = "client_secret_basic"

api = router = TigrblRouter()
_FALLBACK_TOKENS: dict[str, dict[str, Any]] = {}


def _require_tls(request: Request, *, deployment: Any | None = None) -> None:
    scope = getattr(request, "scope", {})
    scheme = scope.get("scheme") if isinstance(scope, dict) else None
    if not scheme:
        try:
            url = request.url
            scheme = url.scheme if hasattr(url, "scheme") else str(url).split(":", 1)[0]
        except Exception:
            scheme = "http"
    active_deployment = deployment or deployment_from_request(request, settings)
    if active_deployment.flag_enabled("require_tls") and scheme != "https":
        raise HTTPException(status.HTTP_400_BAD_REQUEST, {"error": "tls_required"})


def _optional_registration_unavailable(exc: Exception) -> bool:
    message = f"{exc.__class__.__module__}.{exc.__class__.__name__}: {exc}".lower()
    if "has no attribute 'execute'" in message:
        return True
    return any(
        marker in message
        for marker in (
            "undefinedtable",
            "no such table",
            "missing table",
        )
    ) or ("does not exist" in message and ("relation" in message or "table" in message))


async def _load_client(db: Any, client_id: str) -> tuple[Client | None, ClientRegistration | None]:
    try:
        client_key: UUID | str = UUID(str(client_id))
    except ValueError:
        client_key = client_id
    client = await read_handler_record(Client, db, client_key)
    registration = None
    if client is not None:
        try:
            registration = await first_handler_record(ClientRegistration, db, {"client_id": client.id})
        except Exception as exc:
            if not _optional_registration_unavailable(exc):
                raise
    return client, registration


def _registered_token_endpoint_auth_method(registration: ClientRegistration | None) -> str:
    raw_metadata = getattr(registration, "registration_metadata", None) if registration is not None else None
    metadata = raw_metadata if isinstance(raw_metadata, dict) else {}
    return str(metadata.get("token_endpoint_auth_method") or DEFAULT_TOKEN_ENDPOINT_AUTH_METHOD)


def _introspect_token(token: str) -> Dict[str, Any]:
    return run_async(_introspect_token_async(token))


def _record_token(token: str, claims: Dict[str, Any], token_kind: str | None = None) -> str:
    return run_async(_record_token_async(token, claims, token_kind=token_kind))


def _unregister_token(token: str) -> None:
    return run_async(remove_token_record_async(token))


def _protected_resource_verifier_contract(request: Any):
    return protected_resource_verifier_contract_from_request(request)


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
    registration_metadata = raw_registration_metadata if isinstance(raw_registration_metadata, dict) else {}

    if client_assertion:
        if PRIVATE_KEY_JWT_AUTH_METHOD not in allowed_auth_methods or registered_auth_method != PRIVATE_KEY_JWT_AUTH_METHOD:
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
                presented_certificate_pem=presented_certificate_pem(request),
                token_endpoint_auth_method=registered_auth_method,
            )
        except ValueError as exc:
            raise HTTPException(int(_HTTPStatus.UNAUTHORIZED), "invalid_client") from exc
        return None

    if registered_auth_method == "client_secret_post":
        if registered_auth_method not in allowed_auth_methods or not client_secret:
            raise HTTPException(int(_HTTPStatus.UNAUTHORIZED), "invalid_client")
    elif registered_auth_method == "client_secret_basic":
        if registered_auth_method not in allowed_auth_methods or not auth.startswith("Basic ") or not client_secret:
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


def unregister_token(token: str) -> None:
    _FALLBACK_TOKENS.pop(token, None)
    _unregister_token(token)


def introspect_token(token: str) -> Dict[str, Any]:
    if not settings.enable_rfc7662:
        raise RuntimeError(f"RFC 7662 support is disabled: {RFC7662_SPEC_URL}")
    payload = _introspect_token(token)
    if payload.get("active") is False and token in _FALLBACK_TOKENS:
        payload = {"active": True, **_FALLBACK_TOKENS[token]}
    return _apply_introspection_activity_constraints(payload)


async def introspect_token_async(token: str) -> Dict[str, Any]:
    if not settings.enable_rfc7662:
        raise RuntimeError(f"RFC 7662 support is disabled: {RFC7662_SPEC_URL}")
    payload = await _introspect_token_async(token)
    if payload.get("active") is False and token in _FALLBACK_TOKENS:
        payload = {"active": True, **_FALLBACK_TOKENS[token]}
    return _apply_introspection_activity_constraints(payload)


def reset_tokens() -> None:
    _FALLBACK_TOKENS.clear()
    _reset_token_state()


async def reset_tokens_async() -> None:
    _FALLBACK_TOKENS.clear()
    await _reset_token_state_async()


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


@api.route("/introspect", methods=["POST"], response_model=IntrospectOut)
async def introspect(request: Request, db: AsyncSession = Depends(get_db)):
    deployment = deployment_from_request(request, settings)
    _require_tls(request, deployment=deployment)
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
