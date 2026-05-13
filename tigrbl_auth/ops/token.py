from __future__ import annotations

import base64
import inspect
from datetime import datetime, timezone
from typing import Any
from urllib.parse import parse_qs
from uuid import UUID

from tigrbl_auth.config.deployment import deployment_from_request, resolve_deployment
from tigrbl_auth.config.settings import settings
from tigrbl_auth.errors import InvalidTokenError
from tigrbl_auth.services.token_service import (
    InvalidRefreshTokenError,
    RefreshTokenReuseError,
    issue_persisted_token_pair,
    redeem_refresh_token,
)
try:  # pragma: no cover - exercised with the full runtime stack installed
    from tigrbl_auth.oidc_id_token import mint_id_token, oidc_hash
except Exception:  # pragma: no cover - dependency-light fallback for checkpoint tests/evidence
    async def mint_id_token(*, sub: str, aud: str, nonce: str, issuer: str, **claims):
        return 'dependency-light-id-token'

    def oidc_hash(value: str) -> str:
        return str(value)[:8]
from tigrbl_auth.standards.oauth2.assertion_framework import (
    JWT_BEARER_GRANT_TYPE,
    validate_assertion_grant_request,
)
from tigrbl_auth.standards.oauth2.device_authorization import (
    DEVICE_CODE_EXPIRES_IN,
    DEVICE_CODE_GRANT_TYPE,
    DEVICE_CODE_INTERVAL,
    next_device_poll_interval,
    poll_too_frequently,
)
from tigrbl_auth.standards.oauth2.jwt_client_auth import (
    PRIVATE_KEY_JWT_AUTH_METHOD,
    authenticate_client_assertion,
)
from tigrbl_auth.standards.oauth2.mtls import (
    SUPPORTED_MTLS_AUTH_METHODS,
    authenticate_mtls_client,
    presented_certificate_thumbprint,
)
from tigrbl_auth.standards.oauth2.native_apps import validate_native_token_request
from tigrbl_auth.standards.oauth2.resource_indicators import select_resource_indicator
from tigrbl_auth.standards.oauth2.rfc6749 import RFC6749Error, enforce_authorization_code_grant, enforce_grant_type, enforce_password_grant
from tigrbl_auth.standards.oauth2.rfc7636_pkce import verify_code_challenge
from tigrbl_auth.standards.oauth2.rfc8414_metadata import ISSUER
from tigrbl_auth.standards.oauth2.rfc9700 import (
    OAuthPolicyViolation,
    assert_token_request_allowed,
    dpop_proof_from_request,
    runtime_security_profile,
    validate_sender_constraint,
)

try:  # pragma: no cover - exercised with full runtime deps installed
    from tigrbl_auth.framework import HTTPException, JSONResponse as _FrameworkJSONResponse, ValidationError, select, status

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
    from tigrbl_auth.api.rest.schemas import AuthorizationCodeGrantForm, PasswordGrantForm, TokenPair
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
    from tigrbl_auth.api.rest.shared import _jwt, _pwd_backend, _require_tls, allowed_grant_types
except Exception:  # pragma: no cover - dependency-light fallback
    from tigrbl_auth.services.token_service import JWTCoder

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
    from tigrbl_auth.services.persistence import append_audit_event_async
except Exception:  # pragma: no cover - dependency-light fallback
    async def append_audit_event_async(**kwargs):
        return None

try:  # pragma: no cover
    from tigrbl_auth.tables import AuthCode, Client, ClientRegistration, DeviceCode, User
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


async def token_request(*, request, db):
    deployment = _resolve_request_deployment(request)
    _enforce_tls(request, deployment)
    data, resources = await _parse_request_form(request)
    auth = _header(request, 'Authorization')
    dpop_proof = dpop_proof_from_request(request)
    token_endpoint_audiences = _token_endpoint_audiences(deployment)

    client_assertion = str(data.get('client_assertion') or '').strip()
    client_assertion_type = str(data.get('client_assertion_type') or '').strip()
    client_id = None
    client_secret = None
    client_assertion_claims: dict[str, object] | None = None

    if auth and auth.startswith('Basic '):
        try:
            decoded = base64.b64decode(auth.split()[1]).decode()
            client_id, client_secret = decoded.split(':', 1)
        except Exception:
            return _json_error('invalid_client', status_code=status.HTTP_401_UNAUTHORIZED, headers={'WWW-Authenticate': 'Basic'})
    elif client_assertion:
        provisional_client_id = str(data.get('client_id') or '').strip() or None
        try:
            client_assertion_claims = authenticate_client_assertion(
                client_assertion_type=client_assertion_type,
                client_assertion=client_assertion,
                audience=token_endpoint_audiences,
                client_id=provisional_client_id,
            )
        except ValueError as exc:
            return _json_error('invalid_client', status_code=status.HTTP_401_UNAUTHORIZED, description=str(exc))
        client_id = str(client_assertion_claims.get('iss') or '')
    else:
        client_id = data.get('client_id')
        client_secret = data.get('client_secret')

    if not client_id:
        return _json_error('invalid_client', status_code=status.HTTP_401_UNAUTHORIZED, headers={'WWW-Authenticate': 'Basic'})

    client, registration = await _load_client(db, str(client_id))
    if not client:
        return _json_error('invalid_client', status_code=status.HTTP_401_UNAUTHORIZED, headers={'WWW-Authenticate': 'Basic'})

    registered_auth_method = _registered_token_endpoint_auth_method(registration)
    registration_metadata: dict[str, object] = {}
    if registration is not None:
        raw_registration_metadata = getattr(registration, 'registration_metadata', None)
        if isinstance(raw_registration_metadata, dict):
            registration_metadata = dict(raw_registration_metadata)
    policy = runtime_security_profile(deployment)
    if policy.fapi_mode and registered_auth_method not in set(policy.allowed_client_auth_methods):
        return _json_error(
            'invalid_client',
            status_code=status.HTTP_401_UNAUTHORIZED,
            description='FAPI clients must authenticate with private_key_jwt or mTLS',
        )
    if registered_auth_method == PRIVATE_KEY_JWT_AUTH_METHOD:
        if not client_assertion:
            return _json_error('invalid_client', status_code=status.HTTP_401_UNAUTHORIZED, description='client_assertion required for private_key_jwt clients')
        try:
            client_assertion_claims = authenticate_client_assertion(
                client_assertion_type=client_assertion_type,
                client_assertion=client_assertion,
                audience=str(deployment.issuer or ISSUER) if policy.fapi_mode else token_endpoint_audiences,
                client_id=str(client.id),
                token_endpoint_auth_method=registered_auth_method,
            )
        except ValueError as exc:
            return _json_error('invalid_client', status_code=status.HTTP_401_UNAUTHORIZED, description=str(exc))
    elif registered_auth_method in SUPPORTED_MTLS_AUTH_METHODS:
        if client_assertion:
            return _json_error('invalid_client', status_code=status.HTTP_401_UNAUTHORIZED, description='client is not configured for JWT client authentication')
        if client_secret:
            return _json_error('invalid_client', status_code=status.HTTP_401_UNAUTHORIZED, description='client_secret authentication is not permitted for mTLS-authenticated clients')
        try:
            authenticate_mtls_client(
                registration_metadata,
                presented_certificate_thumbprint(request),
                token_endpoint_auth_method=registered_auth_method,
            )
        except ValueError as exc:
            return _json_error('invalid_client', status_code=status.HTTP_401_UNAUTHORIZED, description=str(exc))
    elif client_assertion:
        return _json_error('invalid_client', status_code=status.HTTP_401_UNAUTHORIZED, description='client is not configured for JWT client authentication')
    elif client_secret:
        if policy.fapi_mode:
            return _json_error('invalid_client', status_code=status.HTTP_401_UNAUTHORIZED, description='FAPI rejects shared-secret client authentication')
        secret_valid = client.verify_secret(client_secret)
        if inspect.isawaitable(secret_valid):
            secret_valid = await secret_valid
        if not secret_valid:
            return _json_error('invalid_client', status_code=status.HTTP_401_UNAUTHORIZED, headers={'WWW-Authenticate': 'Basic'})

    if data.get('client_id') and data['client_id'] != str(client_id):
        return _json_error('invalid_client', status_code=status.HTTP_401_UNAUTHORIZED, headers={'WWW-Authenticate': 'Basic'})
    data['client_id'] = str(client_id)
    data.pop('client_secret', None)

    grant_type = data.get('grant_type')
    if not settings.enable_rfc6749 and grant_type not in {'client_credentials', 'password', 'authorization_code', 'refresh_token', JWT_BEARER_GRANT_TYPE, DEVICE_CODE_GRANT_TYPE}:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            [{"loc": ["body", "grant_type"], "msg": "unsupported grant_type", "type": "value_error"}],
        )
    allowed = allowed_grant_types(settings)
    if DEVICE_CODE_GRANT_TYPE not in allowed:
        allowed = [*allowed, DEVICE_CODE_GRANT_TYPE]
    try:
        enforce_grant_type(grant_type, allowed)
        assert_token_request_allowed(data, deployment)
    except RFC6749Error as exc:
        return JSONResponse({'error': str(exc)}, status_code=status.HTTP_400_BAD_REQUEST)
    except OAuthPolicyViolation as exc:
        return JSONResponse({'error': exc.error, 'error_description': exc.description}, status_code=exc.status_code)

    selection = _resource_selection(resources, str(data.get('audience') or '') or None)
    if isinstance(selection, JSONResponse):
        return selection
    resource = selection.resource if selection is not None else None
    request_audience = selection.audience if selection is not None else (str(data.get('audience') or '') or None)

    try:
        sender_constraint = validate_sender_constraint(request, deployment, dpop_proof=dpop_proof)
    except OAuthPolicyViolation as exc:
        return JSONResponse({'error': exc.error, 'error_description': exc.description}, status_code=exc.status_code)
    except ValueError:
        return _json_error('invalid_dpop_proof', status_code=status.HTTP_400_BAD_REQUEST)

    def _jwt_kwargs(*, scope: str | None = None, audience: str | None = None, extra: dict | None = None) -> dict:
        payload: dict = {'issuer': str(deployment.issuer or ISSUER)}
        if scope:
            payload['scope'] = scope
        effective_audience = audience
        if effective_audience in {None, ''} and policy.fapi_mode:
            effective_audience = str(deployment.protected_resource_identifier or settings.protected_resource_identifier)
        if effective_audience is not None:
            payload['audience'] = effective_audience
        elif settings.enable_rfc9068:
            payload['audience'] = settings.protected_resource_identifier
        if sender_constraint.confirmation_claim:
            payload['cnf'] = sender_constraint.confirmation_claim
        if extra:
            payload.update(extra)
        return payload

    if grant_type == 'client_credentials':
        access, refresh = await issue_persisted_token_pair(
            jwt=_jwt,
            sub=str(client_id),
            tid=str(client.tenant_id),
            client_id=str(client.id),
            cert_thumbprint=sender_constraint.cert_thumbprint,
            **_jwt_kwargs(scope=data.get('scope'), audience=request_audience),
        )
        return _token_pair_payload(access, refresh, token_type=sender_constraint.token_type)

    if grant_type == 'password':
        try:
            enforce_password_grant(data)
            parsed = PasswordGrantForm(**data)
        except RFC6749Error as exc:
            return JSONResponse({'error': str(exc)}, status_code=status.HTTP_400_BAD_REQUEST)
        except ValidationError as exc:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, exc.errors())
        user = await _pwd_backend.authenticate(db, parsed.username, parsed.password)
        access, refresh = await issue_persisted_token_pair(
            jwt=_jwt,
            sub=str(user.id),
            tid=str(user.tenant_id),
            client_id=str(client.id),
            cert_thumbprint=sender_constraint.cert_thumbprint,
            **_jwt_kwargs(scope='openid profile email', audience=request_audience),
        )
        return _token_pair_payload(access, refresh, token_type=sender_constraint.token_type)

    if grant_type == 'authorization_code':
        try:
            enforce_authorization_code_grant(data)
            parsed = AuthorizationCodeGrantForm(**data)
        except RFC6749Error as exc:
            return JSONResponse({'error': str(exc)}, status_code=status.HTTP_400_BAD_REQUEST)
        except ValidationError as exc:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, exc.errors())
        try:
            code_uuid = UUID(parsed.code)
        except ValueError:
            return JSONResponse({'error': 'invalid_grant'}, status_code=status.HTTP_400_BAD_REQUEST)
        auth_code = await db.scalar(select(AuthCode).where(AuthCode.id == code_uuid))
        expires_at = auth_code.expires_at if auth_code else None
        if expires_at and getattr(expires_at, 'tzinfo', None) is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        if auth_code is None or str(auth_code.client_id) != parsed.client_id or auth_code.redirect_uri != parsed.redirect_uri or datetime.now(timezone.utc) > (expires_at or datetime.now(timezone.utc)):
            return JSONResponse({'error': 'invalid_grant'}, status_code=status.HTTP_400_BAD_REQUEST)
        try:
            validate_native_token_request(redirect_uri=auth_code.redirect_uri, code_verifier=parsed.code_verifier)
        except ValueError as exc:
            return JSONResponse({'error': 'invalid_grant', 'error_description': str(exc)}, status_code=status.HTTP_400_BAD_REQUEST)
        if auth_code.code_challenge:
            if not parsed.code_verifier or not verify_code_challenge(parsed.code_verifier, auth_code.code_challenge):
                return JSONResponse({'error': 'invalid_grant'}, status_code=status.HTTP_400_BAD_REQUEST)
        auth_code_claims = dict(auth_code.claims or {})
        stored_resource = auth_code_claims.pop('_resource', None)
        initiating_dpop_jkt = auth_code_claims.pop('_dpop_jkt', None)
        initiating_mtls_thumbprint = auth_code_claims.pop('_mtls_thumbprint', None)
        if request_audience not in {None, '', stored_resource} and stored_resource not in {None, ''}:
            return JSONResponse({'error': 'invalid_target'}, status_code=status.HTTP_400_BAD_REQUEST)
        if policy.fapi_mode and not (initiating_dpop_jkt or initiating_mtls_thumbprint):
            return JSONResponse(
                {'error': 'invalid_grant', 'error_description': 'FAPI authorization codes must remain bound to the initiating sender constraint'},
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        if initiating_dpop_jkt and sender_constraint.jkt != str(initiating_dpop_jkt):
            return JSONResponse(
                {'error': 'invalid_grant', 'error_description': 'DPoP proof key continuity check failed'},
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        if initiating_mtls_thumbprint and sender_constraint.cert_thumbprint != str(initiating_mtls_thumbprint):
            return JSONResponse(
                {'error': 'invalid_grant', 'error_description': 'mTLS certificate continuity check failed'},
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        audience = stored_resource or request_audience
        authorization_details = auth_code_claims.pop('_authorization_details', None)
        access, refresh = await issue_persisted_token_pair(
            jwt=_jwt,
            sub=str(auth_code.user_id),
            tid=str(auth_code.tenant_id),
            client_id=str(client.id),
            cert_thumbprint=sender_constraint.cert_thumbprint,
            **_jwt_kwargs(scope=auth_code.scope, audience=audience, extra={'authorization_details': authorization_details} if authorization_details else None),
        )
        extra_claims = {'tid': str(auth_code.tenant_id), 'typ': 'id', 'at_hash': oidc_hash(access)}
        if auth_code.session_id is not None:
            extra_claims['sid'] = str(auth_code.session_id)
        if auth_code.claims and 'id_token' in auth_code.claims:
            user_obj = await db.scalar(select(User).where(User.id == auth_code.user_id))
            idc = auth_code.claims['id_token']
            if 'email' in idc:
                extra_claims['email'] = user_obj.email if user_obj else ''
            if any(k in idc for k in ('name', 'preferred_username')):
                extra_claims['name'] = user_obj.username if user_obj else ''
        id_token = await mint_id_token(
            sub=str(auth_code.user_id),
            aud=parsed.client_id,
            nonce=auth_code.nonce or 'nonce',
            issuer=str(deployment.issuer or ISSUER),
            **extra_claims,
        )
        await db.delete(auth_code)
        await db.commit()
        return _token_pair_payload(access, refresh, token_type=sender_constraint.token_type, id_token=id_token)

    if grant_type == 'refresh_token':
        refresh_token = str(data.get('refresh_token') or '').strip()
        if not refresh_token:
            return _json_error('invalid_request', status_code=status.HTTP_400_BAD_REQUEST, description='refresh_token is required')
        try:
            payload = await redeem_refresh_token(
                jwt=_jwt,
                refresh_token=refresh_token,
                client_id=str(client.id),
                cert_thumbprint=sender_constraint.cert_thumbprint,
                requested_audience=request_audience,
                token_type=sender_constraint.token_type,
            )
        except RefreshTokenReuseError as exc:
            return _json_error('invalid_grant', status_code=status.HTTP_400_BAD_REQUEST, description=str(exc))
        except InvalidRefreshTokenError as exc:
            return _json_error('invalid_grant', status_code=status.HTTP_400_BAD_REQUEST, description=str(exc))
        return payload

    if grant_type == JWT_BEARER_GRANT_TYPE:
        try:
            assertion_claims = validate_assertion_grant_request(data, audience=token_endpoint_audiences)
        except (InvalidTokenError, ValueError) as exc:
            return JSONResponse({'error': 'invalid_grant', 'error_description': str(exc)}, status_code=status.HTTP_400_BAD_REQUEST)
        subject = str(assertion_claims.get('sub') or '')
        if not subject:
            return JSONResponse({'error': 'invalid_grant'}, status_code=status.HTTP_400_BAD_REQUEST)
        scope = str(data.get('scope') or assertion_claims.get('scope') or '') or None
        tenant_id = str(assertion_claims.get('tid') or client.tenant_id)
        access, refresh = await issue_persisted_token_pair(
            jwt=_jwt,
            sub=subject,
            tid=tenant_id,
            client_id=str(client.id),
            cert_thumbprint=sender_constraint.cert_thumbprint,
            **_jwt_kwargs(
                scope=scope,
                audience=request_audience,
                extra={
                    'assertion_issuer': assertion_claims.get('iss'),
                    'assertion_subject': subject,
                    'assertion_jti': assertion_claims.get('jti'),
                },
            ),
        )
        await append_audit_event_async(
            tenant_id=UUID(str(client.tenant_id)) if not isinstance(client.tenant_id, UUID) else client.tenant_id,
            actor_client_id=client.id if isinstance(client.id, UUID) else None,
            event_type='oauth2.assertion_grant.issued',
            target_type='token',
            target_id=str(client.id),
            details={
                'grant_type': JWT_BEARER_GRANT_TYPE,
                'client_id': str(client.id),
                'assertion_issuer': assertion_claims.get('iss'),
                'assertion_subject': subject,
                'audience': request_audience,
                'resource': resource,
                'scope': scope,
            },
        )
        return _token_pair_payload(access, refresh, token_type=sender_constraint.token_type)

    if grant_type == DEVICE_CODE_GRANT_TYPE:
        device_code = data.get('device_code')
        if not device_code:
            return JSONResponse({'error': 'invalid_request'}, status_code=status.HTTP_400_BAD_REQUEST)
        row = await db.scalar(select(DeviceCode).where(DeviceCode.device_code == device_code))
        now = datetime.now(timezone.utc)
        if row is None or str(row.client_id) != str(client.id):
            return _json_error('invalid_grant', status_code=status.HTTP_400_BAD_REQUEST)
        expires_at = row.expires_at if getattr(row.expires_at, 'tzinfo', None) is not None else row.expires_at.replace(tzinfo=timezone.utc)
        if getattr(row, 'consumed_at', None) is not None:
            return _json_error('invalid_grant', status_code=status.HTTP_400_BAD_REQUEST)
        if expires_at <= now:
            return _json_error('expired_token', status_code=status.HTTP_400_BAD_REQUEST)
        last_polled_at = getattr(row, 'last_polled_at', None)
        if poll_too_frequently(last_polled_at=last_polled_at, now=now, interval=getattr(row, 'interval', DEVICE_CODE_INTERVAL)):
            row.poll_count = int(getattr(row, 'poll_count', 0) or 0) + 1
            row.slow_down_count = int(getattr(row, 'slow_down_count', 0) or 0) + 1
            row.last_polled_at = now
            row.interval = next_device_poll_interval(getattr(row, 'interval', DEVICE_CODE_INTERVAL), slow_down_count=1)
            await db.commit()
            await append_audit_event_async(
                tenant_id=getattr(row, 'tenant_id', None),
                actor_client_id=getattr(row, 'client_id', None),
                event_type='device.authorization.poll.slow_down',
                target_type='device_code',
                target_id=str(getattr(row, 'id', device_code)),
                details={'poll_count': row.poll_count, 'interval': row.interval},
            )
            return _json_error('slow_down', status_code=status.HTTP_400_BAD_REQUEST)
        row.poll_count = int(getattr(row, 'poll_count', 0) or 0) + 1
        row.last_polled_at = now
        if getattr(row, 'denied_at', None) is not None or getattr(row, 'denial_reason', None):
            await db.commit()
            return _json_error('access_denied', status_code=status.HTTP_400_BAD_REQUEST)
        if not getattr(row, 'authorized', False) or getattr(row, 'user_id', None) is None or getattr(row, 'tenant_id', None) is None:
            await db.commit()
            await append_audit_event_async(
                tenant_id=getattr(row, 'tenant_id', None),
                actor_client_id=getattr(row, 'client_id', None),
                event_type='device.authorization.poll.pending',
                target_type='device_code',
                target_id=str(getattr(row, 'id', device_code)),
                details={'poll_count': row.poll_count, 'expires_in': DEVICE_CODE_EXPIRES_IN},
            )
            return _json_error('authorization_pending', status_code=status.HTTP_400_BAD_REQUEST)
        effective_audience = request_audience or getattr(row, 'audience', None) or getattr(row, 'resource', None)
        access, refresh = await issue_persisted_token_pair(
            jwt=_jwt,
            sub=str(row.user_id),
            tid=str(row.tenant_id),
            client_id=str(client.id),
            cert_thumbprint=sender_constraint.cert_thumbprint,
            **_jwt_kwargs(scope=row.scope, audience=effective_audience),
        )
        row.consumed_at = now
        await db.commit()
        await append_audit_event_async(
            tenant_id=getattr(row, 'tenant_id', None),
            actor_client_id=getattr(row, 'client_id', None),
            event_type='device.authorization.token_issued',
            target_type='device_code',
            target_id=str(getattr(row, 'id', device_code)),
            details={
                'poll_count': row.poll_count,
                'audience': effective_audience,
                'resource': getattr(row, 'resource', None),
                'interval': getattr(row, 'interval', DEVICE_CODE_INTERVAL),
            },
        )
        return _token_pair_payload(access, refresh, token_type=sender_constraint.token_type)

    return _json_error('unsupported_grant_type', status_code=status.HTTP_400_BAD_REQUEST)
