"""Runtime collaborators and composition for the RFC 9126 HTTP carrier."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from types import SimpleNamespace
from uuid import UUID

from tigrbl import Request, TigrblApp
from tigrbl.runtime.status import HTTPException, status
from tigrbl_auth_router_oauth_par import (
    build_pushed_authorization_router,
    include_pushed_authorization_endpoint as include_http_par_endpoint,
)
from tigrbl_auth_protocol_oauth.standards.dpop import verify_proof_async
from tigrbl_auth_protocol_oauth.standards.jwt_client_auth import (
    PRIVATE_KEY_JWT_AUTH_METHOD,
    authenticate_client_assertion,
)
from tigrbl_auth_protocol_oauth.standards.jwt_secured_authorization_requests import (
    merge_request_object_params,
    parse_request_object,
)
from tigrbl_auth_protocol_oauth.standards.mutual_tls_client_authentication import (
    SUPPORTED_MTLS_AUTH_METHODS,
    authenticate_mtls_client,
    presented_certificate_pem,
)
from tigrbl_auth_protocol_oauth.standards.oauth_security_bcp import (
    client_certificate_thumbprint_from_request,
    dpop_proof_from_request,
    runtime_security_profile,
)
from tigrbl_auth_protocol_oauth.standards.resource_indicators import (
    select_resource_indicator,
)
from tigrbl_auth_protocol_oauth.standards.rich_authorization_requests import (
    normalize_authorization_details,
)
from tigrbl_identity_contracts.oauth import PushedAuthorizationPersistenceRequest
from tigrbl_identity_runtime.deployment import (
    deployment_from_app,
    deployment_from_request,
    resolve_deployment,
)
from tigrbl_identity_runtime.settings import settings
from tigrbl_identity_storage.tables.client import Client
from tigrbl_identity_storage.tables.client_registration import ClientRegistration
from tigrbl_identity_storage.tables.pushed_authorization_request import (
    DEFAULT_PAR_EXPIRY,
)
from tigrbl_identity_storage_runtime.dpop_state import (
    check_and_store_dpop_replay,
    consume_dpop_nonce,
)
from tigrbl_identity_storage_runtime.engine import get_db
from tigrbl_identity_storage_runtime.ops.common import first_record, read_record

from .security.pushed_authorization import (
    build_rfc9126_pushed_authorization_service,
)


_CLIENT_AUTH_PARAMETERS = frozenset(
    {"client_assertion", "client_assertion_type", "client_secret"}
)


def _header(request: Request, name: str) -> str | None:
    headers = getattr(request, "headers", {}) or {}
    return headers.get(name) or headers.get(name.lower())


def _resolve_request_deployment(request: Request):
    if getattr(request, "app", None) is not None:
        return deployment_from_request(request, settings)
    return resolve_deployment(settings)


async def _normalized_par_params(
    params: Mapping[str, object],
    deployment,
) -> dict[str, object]:
    normalized = dict(params)
    request_object = normalized.get("request")
    if request_object:
        if not deployment.flag_enabled("enable_rfc9101"):
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "request object support disabled",
            )
        try:
            parsed_request = await parse_request_object(
                str(request_object),
                secret=settings.jwt_secret,
                algorithms=("HS256", "HS384", "HS512"),
                expected_client_id=str(normalized.get("client_id") or "") or None,
                expected_audience=str(deployment.issuer or settings.issuer),
            )
            normalized = merge_request_object_params(
                parsed_request,
                normalized,
                allow_query_overrides=("request",),
            )
        except Exception as exc:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "invalid request object",
            ) from exc

    resources = normalized.get("resource")
    if resources not in (None, "", [], (), {}):
        values = resources if isinstance(resources, list) else [resources]
        if not deployment.flag_enabled("enable_rfc8707"):
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "resource indicators disabled",
            )
        try:
            selection = select_resource_indicator(
                [str(item) for item in values],
                audience=str(normalized.get("audience") or "") or None,
            )
        except ValueError as exc:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "invalid_target") from exc
        normalized["resource"] = list(selection.resources)
        if selection.audience:
            normalized["audience"] = selection.audience

    authorization_details = normalized.get("authorization_details")
    if authorization_details not in (None, "", [], (), {}):
        if not deployment.flag_enabled("enable_rfc9396"):
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "authorization_details disabled",
            )
        try:
            binding = normalize_authorization_details(
                authorization_details,
                resource=str(normalized.get("audience") or "") or None,
                audience=str(normalized.get("audience") or "") or None,
            )
        except Exception as exc:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "invalid authorization_details",
            ) from exc
        normalized["authorization_details"] = binding.details
        if binding.audience and normalized.get("audience") in {None, ""}:
            normalized["audience"] = binding.audience
        if binding.resource and normalized.get("resource") in (
            None,
            "",
            [],
            (),
            {},
        ):
            normalized["resource"] = [binding.resource]
    return normalized


async def normalize_pushed_authorization_request(
    request: Request,
    params: Mapping[str, object],
) -> Mapping[str, object]:
    return await _normalized_par_params(params, _resolve_request_deployment(request))


async def _authenticate_fapi_par_client(
    *,
    request: Request,
    db,
    params: Mapping[str, object],
    deployment,
):
    client_id = str(params.get("client_id") or "").strip()
    try:
        client_uuid = UUID(client_id)
    except (TypeError, ValueError, AttributeError) as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "invalid client_id") from exc
    client = await read_record(Client, db, client_uuid)
    if client is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "client not found")
    registration = await first_record(
        ClientRegistration,
        db,
        {"client_id": client.id},
    )
    metadata = dict(getattr(registration, "registration_metadata", None) or {})
    auth_method = str(metadata.get("token_endpoint_auth_method") or "").strip()
    policy = runtime_security_profile(deployment)
    if auth_method not in set(policy.allowed_client_auth_methods):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "invalid_client_metadata: FAPI clients must use private_key_jwt or mTLS",
        )

    authorization = _header(request, "Authorization")
    client_assertion = str(params.get("client_assertion") or "").strip()
    client_assertion_type = str(
        params.get("client_assertion_type") or ""
    ).strip()
    if authorization and authorization.startswith("Basic "):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            {
                "error": "invalid_client",
                "error_description": "FAPI PAR rejects HTTP Basic client authentication",
            },
        )
    if auth_method == PRIVATE_KEY_JWT_AUTH_METHOD:
        if not client_assertion:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                {
                    "error": "invalid_client",
                    "error_description": "client_assertion required for FAPI PAR",
                },
            )
        try:
            authenticate_client_assertion(
                client_assertion_type=client_assertion_type,
                client_assertion=client_assertion,
                audience=str(deployment.issuer or settings.issuer),
                client_id=str(client.id),
                token_endpoint_auth_method=auth_method,
            )
        except ValueError as exc:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                {"error": "invalid_client", "error_description": str(exc)},
            ) from exc
    elif auth_method in SUPPORTED_MTLS_AUTH_METHODS:
        try:
            authenticate_mtls_client(
                metadata,
                client_certificate_thumbprint_from_request(request),
                presented_certificate_pem=presented_certificate_pem(request),
                token_endpoint_auth_method=auth_method,
            )
        except ValueError as exc:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                {"error": "invalid_client", "error_description": str(exc)},
            ) from exc
    else:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            {
                "error": "invalid_client",
                "error_description": "unsupported FAPI PAR authentication method",
            },
        )
    return client


async def authorize_pushed_authorization_caller(
    request: Request,
    params: Mapping[str, object],
    db,
) -> PushedAuthorizationPersistenceRequest:
    deployment = _resolve_request_deployment(request)
    policy = runtime_security_profile(deployment)
    client_id = str(params.get("client_id") or "").strip()
    if not client_id:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "client_id parameter required",
        )
    if policy.par_redirect_uri_required and not params.get("redirect_uri"):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "redirect_uri parameter required",
        )
    try:
        client_uuid = UUID(client_id)
    except (TypeError, ValueError, AttributeError) as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "invalid client_id") from exc
    client = await read_record(Client, db, client_uuid)
    if client is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "client not found")
    if policy.par_client_auth_required:
        client = await _authenticate_fapi_par_client(
            request=request,
            db=db,
            params=params,
            deployment=deployment,
        )

    persisted_params = {
        key: value
        for key, value in params.items()
        if key not in _CLIENT_AUTH_PARAMETERS
    }
    dpop_proof = dpop_proof_from_request(request)
    if dpop_proof:
        try:
            persisted_params["_dpop_jkt"] = await verify_proof_async(
                dpop_proof,
                getattr(request, "method", "POST"),
                str(getattr(request, "url", "")),
                replay_checker=lambda claims, ttl_s=300: check_and_store_dpop_replay(
                    db,
                    claims,
                    ttl_s=ttl_s,
                ),
                nonce_consumer=lambda nonce, now=None: consume_dpop_nonce(
                    db,
                    nonce,
                    now=now,
                ),
            )
        except ValueError as exc:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                {
                    "error": "invalid_dpop_proof",
                    "error_description": str(exc),
                },
            ) from exc
    cert_thumbprint = client_certificate_thumbprint_from_request(request)
    if cert_thumbprint:
        persisted_params["_mtls_thumbprint"] = cert_thumbprint

    if DEFAULT_PAR_EXPIRY > policy.request_uri_max_lifetime_seconds:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            {
                "error": "invalid_request",
                "error_description": (
                    "request_uri lifetime exceeds the active profile limit"
                ),
            },
        )
    return PushedAuthorizationPersistenceRequest(
        client_id=str(client.id),
        tenant_id=(str(client.tenant_id) if client.tenant_id is not None else None),
        params=persisted_params,
    )


def _service_for_request(request: Request, db):
    deployment = _resolve_request_deployment(request)
    return build_rfc9126_pushed_authorization_service(
        db,
        SimpleNamespace(
            enable_rfc9126=deployment.flag_enabled("enable_rfc9126")
        ),
    )


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[5]


def observe_pushed_authorization_response(
    request: Request,
    payload: Mapping[str, object],
) -> None:
    from tigrbl_identity_storage_runtime.session_service import observe_par_response

    observe_par_response(
        _repo_root(),
        request_uri=payload.get("request_uri"),
        details=dict(payload),
    )


router = build_pushed_authorization_router(
    service_for_request=_service_for_request,
    normalize_request=normalize_pushed_authorization_request,
    authorize_caller=authorize_pushed_authorization_caller,
    observe_response=observe_pushed_authorization_response,
    get_db=get_db,
)


def include_par_endpoint(app: TigrblApp) -> None:
    deployment = deployment_from_app(app, settings)
    include_http_par_endpoint(
        app,
        router,
        enabled=deployment.flag_enabled("enable_rfc9126"),
    )


include_rfc9126 = include_par_endpoint


__all__ = [
    "_normalized_par_params",
    "authorize_pushed_authorization_caller",
    "include_par_endpoint",
    "include_rfc9126",
    "normalize_pushed_authorization_request",
    "observe_pushed_authorization_response",
    "router",
]
