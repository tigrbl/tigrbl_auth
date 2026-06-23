from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import parse_qs
from uuid import UUID

from tigrbl_identity_runtime.deployment import deployment_from_app, deployment_from_request, resolve_deployment
from tigrbl_identity_runtime.settings import settings
from tigrbl_identity_storage.tables._ops import create_record, first_record, read_record
from tigrbl_identity_storage.tables.audit_event import AuditEvent
from tigrbl_auth_protocol_oauth.standards.jwt_secured_authorization_requests import merge_request_object_params, parse_request_object
from tigrbl_auth_protocol_oauth.standards.pushed_authorization_requests import REQUEST_URI_PREFIX
from tigrbl_auth_protocol_oauth.standards.rich_authorization_requests import normalize_authorization_details
from tigrbl_auth_protocol_oauth.standards.resource_indicators import select_resource_indicator
from tigrbl_auth_protocol_oauth.standards.oauth_security_bcp import (
    client_certificate_thumbprint_from_request,
    dpop_proof_from_request,
    runtime_security_profile,
)
from tigrbl_auth_protocol_oauth.standards.jwt_client_auth import (
    PRIVATE_KEY_JWT_AUTH_METHOD,
    authenticate_client_assertion,
)
from tigrbl_auth_protocol_oauth.standards.mutual_tls_client_authentication import (
    SUPPORTED_MTLS_AUTH_METHODS,
    authenticate_mtls_client,
    presented_certificate_pem,
)
from tigrbl_auth_protocol_oauth.standards.dpop import verify_proof

try:  # pragma: no cover - exercised with the full runtime stack installed
    from tigrbl_identity_storage.framework import Depends, HTTPException, TigrblApp, TigrblRouter, status
    from tigrbl_identity_storage.tables.engine import get_db
except Exception:  # pragma: no cover - dependency-light fallback for checkpoint tests/evidence
    class _FallbackStatus:
        HTTP_400_BAD_REQUEST = 400
        HTTP_404_NOT_FOUND = 404
        HTTP_401_UNAUTHORIZED = 401

    class HTTPException(Exception):
        def __init__(self, status_code: int, detail: object):
            super().__init__(detail)
            self.status_code = status_code
            self.detail = detail

    status = _FallbackStatus()
    Depends = lambda dependency: dependency  # type: ignore[assignment]

    class TigrblApp:  # type: ignore[override]
        pass

    class TigrblRouter:  # type: ignore[override]
        def __init__(self, *args, **kwargs):
            self.routes = []

        def route(self, path: str, methods=None, response_model=None, **kwargs):
            def decorator(func):
                self.routes.append(type("Route", (), {"path": path, "methods": methods})())
                return func

            return decorator

    def get_db():  # type: ignore[override]
        return None

try:  # pragma: no cover - exercised with the full runtime stack installed
    from tigrbl_identity_storage.tables.client import Client
    from tigrbl_identity_storage.tables.client_registration import ClientRegistration
    from tigrbl_identity_storage.tables.pushed_authorization_request import (
        PushedAuthorizationRequest,
        PushedAuthorizationResponse,
    )
except Exception:  # pragma: no cover - dependency-light placeholders
    class Client:  # type: ignore[override]
        id = object()
        tenant_id = None

    class ClientRegistration:  # type: ignore[override]
        client_id = object()
        registration_metadata = {}

    class PushedAuthorizationRequest:  # type: ignore[override]
        def __init__(self, *, client_id=None, tenant_id=None, params=None):
            self.id = 'dependency-light-par-row'
            self.client_id = client_id
            self.tenant_id = tenant_id
            self.params = dict(params or {})
            self.request_uri = f'{REQUEST_URI_PREFIX}dependency-light'
            self.expires_in = 90
            self.expires_at = None
            self.consumed_at = None

    class PushedAuthorizationResponse:  # type: ignore[override]
        pass

api = router = TigrblRouter()

def _body_dict(body: bytes) -> dict:
    if not body:
        return {}
    text = body.decode('utf-8')
    try:
        parsed_json = json.loads(text)
        if isinstance(parsed_json, dict):
            return parsed_json
    except Exception:
        pass
    parsed = parse_qs(text, keep_blank_values=True)
    result: dict[str, object] = {}
    for key, values in parsed.items():
        if len(values) == 1:
            result[key] = values[-1]
        else:
            result[key] = list(values)
    return result


async def _normalized_par_params(params: dict[str, object], deployment) -> dict[str, object]:
    normalized = dict(params)
    request_object = normalized.get('request')
    if request_object:
        if not deployment.flag_enabled('enable_rfc9101'):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, 'request object support disabled')
        try:
            parsed_request = await parse_request_object(
                str(request_object),
                secret=settings.jwt_secret,
                algorithms=('HS256', 'HS384', 'HS512'),
                expected_client_id=str(normalized.get('client_id') or '') or None,
                expected_audience=str(deployment.issuer or settings.issuer),
            )
            normalized = merge_request_object_params(parsed_request, normalized, allow_query_overrides=('request',))
        except Exception as exc:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, 'invalid request object') from exc

    resources = normalized.get('resource')
    if resources not in (None, '', [], (), {}):
        values = resources if isinstance(resources, list) else [resources]
        if not deployment.flag_enabled('enable_rfc8707'):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, 'resource indicators disabled')
        try:
            selection = select_resource_indicator([str(item) for item in values], audience=str(normalized.get('audience') or '') or None)
        except ValueError as exc:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, 'invalid_target') from exc
        normalized['resource'] = list(selection.resources)
        if selection.audience:
            normalized['audience'] = selection.audience

    authorization_details = normalized.get('authorization_details')
    if authorization_details not in (None, '', [], (), {}):
        if not deployment.flag_enabled('enable_rfc9396'):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, 'authorization_details disabled')
        try:
            binding = normalize_authorization_details(
                authorization_details,
                resource=str(normalized.get('audience') or '') or None,
                audience=str(normalized.get('audience') or '') or None,
            )
        except Exception as exc:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, 'invalid authorization_details') from exc
        normalized['authorization_details'] = binding.details
        if binding.audience and normalized.get('audience') in {None, ''}:
            normalized['audience'] = binding.audience
        if binding.resource and normalized.get('resource') in (None, '', [], (), {}):
            normalized['resource'] = [binding.resource]
    return normalized


def _header(request, name: str) -> str | None:
    headers = getattr(request, "headers", {}) or {}
    return headers.get(name) or headers.get(name.lower())


def _resolve_request_deployment(request):
    if getattr(request, "app", None) is not None:
        return deployment_from_request(request, settings)
    return resolve_deployment(settings)


async def _authenticate_fapi_par_client(*, request, db, params: dict[str, object], deployment) -> tuple[object, dict[str, object]]:
    client_id = str(params.get("client_id") or "").strip()
    if not client_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "client_id parameter required")
    try:
        client_uuid = UUID(client_id)
    except Exception as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "invalid client_id") from exc
    client = await read_record(Client, db, client_uuid)
    if client is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "client not found")
    registration = await first_record(ClientRegistration, db, {"client_id": client.id})
    metadata = dict(getattr(registration, "registration_metadata", None) or {})
    auth_method = str(metadata.get("token_endpoint_auth_method") or "").strip()
    policy = runtime_security_profile(deployment)
    if auth_method not in set(policy.allowed_client_auth_methods):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "invalid_client_metadata: FAPI clients must use private_key_jwt or mTLS")

    authz = _header(request, "Authorization")
    client_assertion = str(params.get("client_assertion") or "").strip()
    client_assertion_type = str(params.get("client_assertion_type") or "").strip()
    if authz and authz.startswith("Basic "):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, {"error": "invalid_client", "error_description": "FAPI PAR rejects HTTP Basic client authentication"})
    if auth_method == PRIVATE_KEY_JWT_AUTH_METHOD:
        if not client_assertion:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, {"error": "invalid_client", "error_description": "client_assertion required for FAPI PAR"})
        try:
            authenticate_client_assertion(
                client_assertion_type=client_assertion_type,
                client_assertion=client_assertion,
                audience=str(deployment.issuer or settings.issuer),
                client_id=str(client.id),
                token_endpoint_auth_method=auth_method,
            )
        except ValueError as exc:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, {"error": "invalid_client", "error_description": str(exc)}) from exc
    elif auth_method in SUPPORTED_MTLS_AUTH_METHODS:
        try:
            authenticate_mtls_client(
                metadata,
                client_certificate_thumbprint_from_request(request),
                presented_certificate_pem=presented_certificate_pem(request),
                token_endpoint_auth_method=auth_method,
            )
        except ValueError as exc:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, {"error": "invalid_client", "error_description": str(exc)}) from exc
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, {"error": "invalid_client", "error_description": "unsupported FAPI PAR authentication method"})
    return client, metadata


async def pushed_authorization_request(*, request, db):
    deployment = _resolve_request_deployment(request)
    if not deployment.flag_enabled('enable_rfc9126'):
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'PAR disabled')
    params = _body_dict(getattr(request, 'body', b'') or b'')
    params = await _normalized_par_params(params, deployment)
    policy = runtime_security_profile(deployment)
    client_id = params.get('client_id')
    if not client_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'client_id parameter required')
    if policy.par_redirect_uri_required and not params.get("redirect_uri"):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "redirect_uri parameter required")
    try:
        client_uuid = UUID(str(client_id))
    except Exception as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'invalid client_id') from exc
    client = await read_record(Client, db, client_uuid)
    if client is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'client not found')
    if policy.par_client_auth_required:
        client, _ = await _authenticate_fapi_par_client(request=request, db=db, params=params, deployment=deployment)

    dpop_proof = dpop_proof_from_request(request)
    if dpop_proof:
        try:
            params["_dpop_jkt"] = verify_proof(dpop_proof, getattr(request, "method", "POST"), str(getattr(request, "url", "")))
        except ValueError as exc:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, {"error": "invalid_dpop_proof", "error_description": str(exc)}) from exc
    cert_thumbprint = client_certificate_thumbprint_from_request(request)
    if cert_thumbprint:
        params["_mtls_thumbprint"] = cert_thumbprint

    preview = PushedAuthorizationRequest(
        client_id=client.id,
        tenant_id=client.tenant_id,
        params=params,
    )
    if int(getattr(preview, "expires_in", 0) or 0) > policy.request_uri_max_lifetime_seconds:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            {"error": "invalid_request", "error_description": "request_uri lifetime exceeds the active profile limit"},
        )
    row = await create_record(
        PushedAuthorizationRequest,
        db,
        {
            "client_id": client.id,
            "tenant_id": client.tenant_id,
            "params": params,
        },
    )

    await AuditEvent.record(
        db,
        tenant_id=client.tenant_id,
        actor_client_id=client.id,
        event_type='authorization.par.created',
        target_type='par_request',
        target_id=str(row.id),
        details={
            'request_uri': row.request_uri,
            'resource': params.get('resource'),
            'audience': params.get('audience'),
            'authorization_details_present': bool(params.get('authorization_details')),
            'request_object_present': bool(params.get('request')),
        },
    )

    return {'request_uri': row.request_uri, 'expires_in': row.expires_in}


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[5]


@api.route("/par", methods=["POST"], response_model=PushedAuthorizationResponse)
async def par(request, db=Depends(get_db)):
    result = await pushed_authorization_request(request=request, db=db)
    from tigrbl_identity_storage_runtime.session_service import observe_par_response

    payload = result if isinstance(result, dict) else getattr(result, "model_dump", lambda **_: {})(mode="json")
    observe_par_response(_repo_root(), request_uri=payload.get("request_uri"), details=payload)
    return result


def include_par_endpoint(app: TigrblApp) -> None:
    deployment = deployment_from_app(app, settings)
    path = "/par"
    if deployment.route_enabled(path) and not any(
        (getattr(route, "path", None) or getattr(route, "path_template", None)) == path
        for route in app.router.routes
    ):
        app.include_router(api)


include_rfc9126 = include_par_endpoint


__all__ = [
    "api",
    "router",
    "par",
    "pushed_authorization_request",
    "_normalized_par_params",
    "include_par_endpoint",
    "include_rfc9126",
]
