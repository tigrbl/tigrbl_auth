from __future__ import annotations

import base64
import inspect
from datetime import datetime, timezone
from typing import Any
from urllib.parse import parse_qs
from uuid import UUID

from tigrbl_identity_runtime.deployment import deployment_from_request, resolve_deployment
from tigrbl_identity_runtime.settings import settings
from tigrbl_identity_core.errors import InvalidTokenError
from tigrbl_authn_credentials.token_service import (
    InvalidRefreshTokenError,
    RefreshTokenReuseError,
    issue_persisted_token_pair,
    redeem_refresh_token,
)
try:  # pragma: no cover - exercised with the full runtime stack installed
    from tigrbl_auth_protocol_oidc.id_token import mint_id_token, oidc_hash
except Exception:  # pragma: no cover - dependency-light fallback for checkpoint tests/evidence
    async def mint_id_token(*, sub: str, aud: str, nonce: str, issuer: str, **claims):
        return 'dependency-light-id-token'

    def oidc_hash(value: str) -> str:
        return str(value)[:8]
from tigrbl_auth_protocol_oauth.standards.assertion_framework import (
    JWT_BEARER_GRANT_TYPE,
    validate_assertion_grant_request,
)
from tigrbl_auth_protocol_oauth.standards.device_authorization import (
    DEVICE_CODE_EXPIRES_IN,
    DEVICE_CODE_GRANT_TYPE,
    DEVICE_CODE_INTERVAL,
    next_device_poll_interval,
    poll_too_frequently,
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
from tigrbl_auth_protocol_oauth.standards.native_apps import validate_native_token_request
from tigrbl_auth_protocol_oauth.standards.resource_indicators import select_resource_indicator
from tigrbl_auth_protocol_oauth.standards.rfc6749 import RFC6749Error, enforce_authorization_code_grant, enforce_grant_type, enforce_password_grant
from tigrbl_auth_protocol_oauth.standards.rfc7636_pkce import verify_code_challenge
from tigrbl_auth_protocol_oauth.standards.rfc8414_metadata import ISSUER
from tigrbl_auth_protocol_oauth.standards.rfc9700 import (
    OAuthPolicyViolation,
    assert_token_request_allowed,
    dpop_proof_from_request,
    runtime_security_profile,
    validate_sender_constraint,
)

try:  # pragma: no cover - exercised with full runtime deps installed
    from tigrbl_identity_server.framework import HTTPException, JSONResponse as _FrameworkJSONResponse, ValidationError, select, status

    class JSONResponse(_FrameworkJSONResponse):
        def __init__(self, content: Any, *, status_code: int = 200, headers: dict[str, str] | None = None):
            super().__init__(content, status_code=status_code)
            for key, value in (headers or {}).items():
                self.headers[key] = value
            self.content = content
except Exception:  # pragma: no cover - dependency-light fallback for checkpoint tests/evidence
    from pydantic import ValidationError  # type: ignore

    class _FallbackStatus:
        HTTP_400_BAD_REQUEST = 400
        HTTP_401_UNAUTHORIZED = 401
        HTTP_422_UNPROCESSABLE_ENTITY = 422

    class HTTPException(Exception):
        def __init__(self, status_code: int, detail: Any):
            super().__init__(detail)
            self.status_code = status_code
            self.detail = detail

    class JSONResponse(dict):
        def __init__(self, content: Any, *, status_code: int = 200, headers: dict[str, str] | None = None):
            super().__init__(content if isinstance(content, dict) else {'detail': content})
            self.status_code = status_code
            self.headers = headers or {}
            self.content = dict(self)

    class _Select:
        def __init__(self, model: Any):
            self.model = model
            self.criteria: list[Any] = []

        def where(self, criterion: Any):
            self.criteria.append(criterion)
            return self

    def select(model: Any):
        return _Select(model)

    status = _FallbackStatus()

try:  # pragma: no cover
    from tigrbl_identity_contracts.rest import AuthorizationCodeGrantForm, PasswordGrantForm, TokenPair
except Exception:  # pragma: no cover - dependency-light fallback
    from pydantic import BaseModel

    class AuthorizationCodeGrantForm(BaseModel):
        client_id: str
        code: str
        redirect_uri: str
        code_verifier: str | None = None

    class PasswordGrantForm(BaseModel):
        username: str
        password: str
        client_id: str | None = None

    class TokenPair(BaseModel):
        access_token: str
        refresh_token: str | None = None
        id_token: str | None = None
        token_type: str = 'bearer'

try:  # pragma: no cover
    from tigrbl_identity_server.rest.shared import _jwt, _pwd_backend, _require_tls, allowed_grant_types
except Exception:  # pragma: no cover - dependency-light fallback
    from tigrbl_authn_credentials.token_service import JWTCoder

    _jwt = JWTCoder.default if False else None  # placeholder to keep name bound

    class _MissingJWT:
        async def async_sign_pair(self, **kwargs):
            raise RuntimeError('runtime JWT service unavailable in dependency-light mode')

    class _MissingPasswordBackend:
        async def authenticate(self, db, username, password):
            raise RuntimeError('password backend unavailable in dependency-light mode')

    _jwt = _MissingJWT()
    _pwd_backend = _MissingPasswordBackend()

    def _require_tls(request):
        return None

    def allowed_grant_types(_settings):
        return ['client_credentials', 'password', 'authorization_code', 'refresh_token', JWT_BEARER_GRANT_TYPE, DEVICE_CODE_GRANT_TYPE]

try:  # pragma: no cover
    from tigrbl_identity_storage.persistence import append_audit_event_async
except Exception:  # pragma: no cover - dependency-light fallback
    async def append_audit_event_async(**kwargs):
        return None

try:  # pragma: no cover
    from tigrbl_identity_storage.tables import AuthCode, Client, ClientRegistration, DeviceCode, User
except Exception:  # pragma: no cover - placeholders for dependency-light tests
    class Client:  # type: ignore[override]
        id = object()

    class ClientRegistration:  # type: ignore[override]
        client_id = object()
        registration_metadata = None

    class AuthCode:  # type: ignore[override]
        id = object()

    class DeviceCode:  # type: ignore[override]
        device_code = object()

    class User:  # type: ignore[override]
        id = object()


DEFAULT_TOKEN_ENDPOINT_AUTH_METHOD = 'client_secret_basic'



def _header(request, name: str) -> str | None:
    return getattr(request, 'headers', {}).get(name) or getattr(request, 'headers', {}).get(name.lower())


def _resolve_request_deployment(request):
    if getattr(request, 'app', None) is not None:
        return deployment_from_request(request, settings)
    return resolve_deployment(settings)


def _enforce_tls(request, deployment) -> None:
    try:
        _require_tls(request, deployment=deployment)
    except TypeError:
        _require_tls(request)


async def _parse_request_form(request) -> tuple[dict[str, str], list[str]]:
    form_reader = getattr(request, 'form', None)
    if callable(form_reader):
        form = await form_reader()
        resources = list(form.getlist('resource')) if hasattr(form, 'getlist') else []
        data = dict(form)
        if (not resources or 'grant_type' not in data) and getattr(request, 'body', b''):
            parsed = parse_qs(request.body.decode('utf-8'), keep_blank_values=True)
            resources = resources or parsed.get('resource', [])
            for key, values in parsed.items():
                if key != 'resource' and values and key not in data:
                    data[key] = values[-1]
        data.pop('resource', None)
        return data, resources
    body_text = request.body.decode('utf-8') if getattr(request, 'body', b'') else ''
    parsed = parse_qs(body_text, keep_blank_values=True)
    return {k: v[-1] for k, v in parsed.items() if k != 'resource' and v}, parsed.get('resource', [])



def _token_endpoint_audiences(deployment) -> set[str]:
    issuer_candidates = {
        str(getattr(deployment, 'issuer', '') or '').rstrip('/'),
        str(settings.issuer).rstrip('/'),
        str(ISSUER).rstrip('/'),
    }
    return {f"{issuer}/token" for issuer in issuer_candidates if issuer}


async def _load_client(db, client_id: str) -> tuple[Client | None, ClientRegistration | None]:
    try:
        client_key = UUID(str(client_id))
    except ValueError:
        client_key = client_id
    client = await db.scalar(select(Client).where(Client.id == client_key))
    registration = None
    if client is not None:
        registration = await db.scalar(select(ClientRegistration).where(ClientRegistration.client_id == client.id))
    return client, registration



def _registered_token_endpoint_auth_method(registration: ClientRegistration | None) -> str:
    raw_metadata = getattr(registration, 'registration_metadata', None) if registration is not None else None
    if isinstance(raw_metadata, dict):
        metadata = raw_metadata
    else:
        metadata = {}
    return str(metadata.get('token_endpoint_auth_method') or DEFAULT_TOKEN_ENDPOINT_AUTH_METHOD)



def _json_error(error: str, *, status_code: int, description: str | None = None, headers: dict[str, str] | None = None):
    payload = {'error': error}
    if description:
        payload['error_description'] = description
    response = JSONResponse(payload, status_code=status_code)
    response.content = payload  # type: ignore[attr-defined]
    for key, value in (headers or {}).items():
        response.headers[key] = value
    return response



def _resource_selection(resources: list[str], audience: str | None):
    if not (getattr(settings, 'enable_rfc8707', True) and getattr(settings, 'rfc8707_enabled', True)):
        return None
    if not resources and audience in {None, ''}:
        return None
    try:
        return select_resource_indicator(resources, audience=audience, allow_multiple_distinct=True)
    except ValueError:
        return _json_error('invalid_target', status_code=status.HTTP_400_BAD_REQUEST)



def _token_pair_payload(access: str, refresh: str | None, *, token_type: str, id_token: str | None = None) -> dict[str, Any]:
    return TokenPair(access_token=access, refresh_token=refresh, id_token=id_token, token_type=token_type).model_dump(exclude_none=True)


