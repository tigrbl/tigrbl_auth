"""Runtime collaborators and composition for the RFC 7662 HTTP carrier."""

from __future__ import annotations

import base64
from http import HTTPStatus
from typing import Any, Mapping
from uuid import UUID

from tigrbl import Request, TigrblApp
from tigrbl.engine import HybridSession as AsyncSession
from tigrbl.runtime.status import HTTPException
from tigrbl_auth_api_oauth_introspection import (
    build_introspection_router,
    include_introspection_endpoint as include_http_introspection_endpoint,
)
from tigrbl_auth_protocol_oauth.standards._introspection_activity import header
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
    build_protected_resource_verifier_contract,
)
from tigrbl_identity_runtime.deployment import deployment_from_request
from tigrbl_identity_runtime.settings import settings
from tigrbl_identity_storage.tables.client import Client
from tigrbl_identity_storage.tables.client_registration import ClientRegistration
from tigrbl_identity_storage_runtime.engine import get_db
from tigrbl_identity_storage_runtime.ops.clients import lookup_client
from tigrbl_identity_storage_runtime.ops.common import (
    first_handler_record,
    read_handler_record,
)
from tigrbl_principal_authentication import ClientSecretAuthenticationCapability

from .security.token_introspection import build_rfc7662_introspection_service


DEFAULT_TOKEN_ENDPOINT_AUTH_METHOD = "client_secret_basic"
client_secret_authentication = ClientSecretAuthenticationCapability(lookup_client)


def _require_transport(request: Request) -> None:
    scope = getattr(request, "scope", {})
    scheme = scope.get("scheme") if isinstance(scope, dict) else None
    if not scheme:
        try:
            url = request.url
            scheme = url.scheme if hasattr(url, "scheme") else str(url).split(":", 1)[0]
        except Exception:
            scheme = "http"
    deployment = deployment_from_request(request, settings)
    if deployment.flag_enabled("require_tls") and scheme != "https":
        raise HTTPException(HTTPStatus.BAD_REQUEST, {"error": "tls_required"})


def _optional_registration_unavailable(exc: Exception) -> bool:
    message = f"{exc.__class__.__module__}.{exc.__class__.__name__}: {exc}".lower()
    if "has no attribute 'execute'" in message:
        return True
    return any(
        marker in message
        for marker in ("undefinedtable", "no such table", "missing table")
    ) or ("does not exist" in message and ("relation" in message or "table" in message))


async def _load_client(
    db: Any, client_id: str
) -> tuple[Client | None, ClientRegistration | None]:
    try:
        client_key: UUID | str = UUID(str(client_id))
    except ValueError:
        client_key = client_id
    client = await read_handler_record(Client, db, client_key)
    registration = None
    if client is not None:
        try:
            registration = await first_handler_record(
                ClientRegistration, db, {"client_id": client.id}
            )
        except Exception as exc:
            if not _optional_registration_unavailable(exc):
                raise
    return client, registration


def _registered_auth_method(registration: ClientRegistration | None) -> str:
    raw = getattr(registration, "registration_metadata", None)
    metadata = raw if isinstance(raw, dict) else {}
    return str(
        metadata.get("token_endpoint_auth_method") or DEFAULT_TOKEN_ENDPOINT_AUTH_METHOD
    )


def _protected_resource_verifier_contract(request: Any):
    return build_protected_resource_verifier_contract(
        deployment_from_request(request, settings)
    )


def _introspection_endpoint_audiences(request: Any) -> set[str]:
    deployment = deployment_from_request(request, settings)
    issuer = str(getattr(deployment, "issuer", None) or settings.issuer).rstrip("/")
    return {issuer, f"{issuer}/introspect", f"{issuer}/token"} - {""}


async def authorize_introspection_caller(
    request: Request,
    form_data: Mapping[str, object],
    db: AsyncSession,
) -> None:
    contract = _protected_resource_verifier_contract(request)
    allowed_auth_methods = set(contract.introspection_auth_methods)
    authorization = header(request, "Authorization") or ""
    client_assertion = str(form_data.get("client_assertion") or "").strip()
    client_assertion_type = str(form_data.get("client_assertion_type") or "").strip()
    client_id: str | None = None
    client_secret: str | None = None

    if authorization.startswith("Basic "):
        try:
            decoded = base64.b64decode(authorization.split()[1]).decode()
            client_id, client_secret = decoded.split(":", 1)
        except Exception as exc:
            raise HTTPException(HTTPStatus.UNAUTHORIZED, "invalid_client") from exc
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
            raise HTTPException(HTTPStatus.UNAUTHORIZED, "invalid_client") from exc
        client_id = str(claims.get("iss") or "").strip() or None

    if not client_id:
        raise HTTPException(
            HTTPStatus.UNAUTHORIZED,
            "authenticated caller required",
        )

    client, registration = await _load_client(db, client_id)
    if client is None:
        raise HTTPException(HTTPStatus.UNAUTHORIZED, "invalid_client")

    registered_auth_method = _registered_auth_method(registration)
    raw_metadata = getattr(registration, "registration_metadata", None)
    registration_metadata = raw_metadata if isinstance(raw_metadata, dict) else {}

    if client_assertion:
        if (
            PRIVATE_KEY_JWT_AUTH_METHOD not in allowed_auth_methods
            or registered_auth_method != PRIVATE_KEY_JWT_AUTH_METHOD
        ):
            raise HTTPException(HTTPStatus.UNAUTHORIZED, "invalid_client")
        try:
            authenticate_client_assertion(
                client_assertion_type=client_assertion_type,
                client_assertion=client_assertion,
                audience=_introspection_endpoint_audiences(request),
                client_id=str(client.id),
                token_endpoint_auth_method=registered_auth_method,
            )
        except ValueError as exc:
            raise HTTPException(HTTPStatus.UNAUTHORIZED, "invalid_client") from exc
        return None

    if registered_auth_method in SUPPORTED_MTLS_AUTH_METHODS:
        if registered_auth_method not in allowed_auth_methods:
            raise HTTPException(HTTPStatus.UNAUTHORIZED, "invalid_client")
        try:
            authenticate_mtls_client(
                registration_metadata,
                presented_certificate_thumbprint(request),
                presented_certificate_pem=presented_certificate_pem(request),
                token_endpoint_auth_method=registered_auth_method,
            )
        except ValueError as exc:
            raise HTTPException(HTTPStatus.UNAUTHORIZED, "invalid_client") from exc
        return None

    if registered_auth_method == "client_secret_post":
        valid_shape = registered_auth_method in allowed_auth_methods and bool(
            client_secret
        )
    elif registered_auth_method == "client_secret_basic":
        valid_shape = (
            registered_auth_method in allowed_auth_methods
            and authorization.startswith("Basic ")
            and bool(client_secret)
        )
    else:
        valid_shape = False
    if not valid_shape:
        raise HTTPException(HTTPStatus.UNAUTHORIZED, "invalid_client")

    result = client_secret_authentication.verify_client_record(client, client_secret)
    if not result.authenticated:
        raise HTTPException(HTTPStatus.UNAUTHORIZED, "invalid_client")


def _service_for_request(request: Request):
    return build_rfc7662_introspection_service(settings)


router = build_introspection_router(
    service_for_request=_service_for_request,
    authorize_caller=authorize_introspection_caller,
    require_transport=_require_transport,
    get_db=get_db,
)


def include_introspection_endpoint(app: TigrblApp) -> None:
    include_http_introspection_endpoint(
        app,
        router,
        enabled=bool(settings.enable_rfc7662),
    )


include_rfc7662 = include_introspection_endpoint


__all__ = [
    "authorize_introspection_caller",
    "include_introspection_endpoint",
    "include_rfc7662",
    "router",
]
