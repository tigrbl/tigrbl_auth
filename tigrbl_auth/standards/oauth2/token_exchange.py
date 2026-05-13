"""RFC 8693 token-exchange route for the release path."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Final
from urllib.parse import parse_qs

from tigrbl_auth.config.deployment import resolve_deployment
from tigrbl_auth.config.settings import settings
from tigrbl_auth.config.deployment import deployment_from_request
from tigrbl_auth.errors import InvalidTokenError
from tigrbl_auth.services.token_service import JWTCoder
from tigrbl_auth.standards.oauth2.resource_indicators import select_resource_indicator
from tigrbl_auth.standards.oauth2.rfc8414_metadata import ISSUER
from tigrbl_auth.standards.oauth2.rfc9700 import (
    TOKEN_EXCHANGE_GRANT_TYPE,
    OAuthPolicyViolation,
    dpop_proof_from_request,
    validate_sender_constraint,
)

try:  # pragma: no cover - exercised with the full runtime stack installed
    from tigrbl_auth.framework import Header, HTTPException, Request, TigrblApp, TigrblRouter, status
except Exception:  # pragma: no cover - dependency-light fallback for checkpoint tests/evidence
    class _FallbackStatus:
        HTTP_400_BAD_REQUEST = 400
        HTTP_404_NOT_FOUND = 404

    def Header(default: Any = None, alias: str | None = None):
        return default

    class HTTPException(Exception):
        def __init__(self, status_code: int, detail: Any):
            super().__init__(detail)
            self.status_code = status_code
            self.detail = detail

    class Request:  # minimal typing aid
        body: bytes
        method: str
        url: str

    class TigrblRouter:
        def __init__(self):
            self.routes: list[Any] = []

        def route(self, path: str, methods: list[str] | tuple[str, ...]):
            def decorator(func):
                self.routes.append(type('Route', (), {'path': path, 'methods': methods})())
                return func

            return decorator

    class TigrblApp:
        def __init__(self):
            self.router = type('RouterContainer', (), {'routes': []})()

        def include_router(self, router):
            self.router.routes.extend(getattr(router, 'routes', []))

    status = _FallbackStatus()

try:  # pragma: no cover
    from tigrbl_auth.services.persistence import append_audit_event_async
except Exception:  # pragma: no cover - dependency-light fallback
    async def append_audit_event_async(**kwargs):
        return None


RFC8693_SPEC_URL: Final[str] = 'https://www.rfc-editor.org/rfc/rfc8693'
SUPPORTED_REQUESTED_TOKEN_TYPES: Final[tuple[str, ...]] = (
    'urn:ietf:params:oauth:token-type:access_token',
    'access_token',
)


@dataclass(frozen=True, slots=True)
class StandardOwner:
    label: str
    title: str
    runtime_status: str
    public_surface: tuple[str, ...]
    notes: str


OWNER = StandardOwner(
    label='RFC 8693',
    title='OAuth 2.0 Token Exchange',
    runtime_status='lineage-audited-token-exchange-runtime',
    public_surface=('/token/exchange',),
    notes=(
        'Mounted token-exchange endpoint with subject-token validation, optional actor-token '
        'delegation semantics, requested-token-type enforcement, consistent resource/audience '
        'binding, and audit-observable lineage details.'
    ),
)


api = TigrblRouter()
router = api



def _jwt_coder() -> JWTCoder:
    return JWTCoder.default()



def _parse_form(request: Request) -> Dict[str, str | list[str]]:
    body = getattr(request, 'body', b'') or b''
    parsed = parse_qs(body.decode('utf-8'), keep_blank_values=True)
    payload: Dict[str, str | list[str]] = {}
    for key, values in parsed.items():
        payload[key] = values[-1] if len(values) == 1 else values
    return payload



def _normalize_requested_token_type(value: Any) -> str:
    requested = str(value or SUPPORTED_REQUESTED_TOKEN_TYPES[0])
    if requested not in SUPPORTED_REQUESTED_TOKEN_TYPES:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, {'error': 'invalid_request', 'error_description': 'unsupported requested_token_type'})
    return requested



def _actor_claim(actor_claims: dict[str, Any] | None) -> dict[str, str] | None:
    if not actor_claims:
        return None
    actor_sub = str(actor_claims.get('sub') or '')
    if not actor_sub:
        return None
    return {'sub': actor_sub}


@api.route('/token/exchange', methods=['POST'])
async def token_exchange(request: Request, dpop: str | None = Header(None, alias='DPoP')) -> dict[str, Any]:
    deployment = deployment_from_request(request, settings)
    if not deployment.flag_enabled('enable_rfc8693'):
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'RFC 8693 disabled: {RFC8693_SPEC_URL}')
    data = _parse_form(request)
    if data.get('grant_type') != TOKEN_EXCHANGE_GRANT_TYPE:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, {'error': 'unsupported_grant_type'})
    subject_token = data.get('subject_token')
    subject_token_type = data.get('subject_token_type')
    if not subject_token or not subject_token_type:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, {'error': 'invalid_request'})

    requested_token_type = _normalize_requested_token_type(data.get('requested_token_type'))

    jwt = _jwt_coder()
    try:
        subject_claims = await jwt.async_decode(str(subject_token), verify_exp=True)
    except (InvalidTokenError, ValueError) as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, {'error': 'invalid_request', 'error_description': 'invalid subject_token'}) from exc

    actor_claims: dict[str, Any] | None = None
    actor_token = data.get('actor_token')
    if actor_token:
        try:
            actor_claims = await jwt.async_decode(str(actor_token), verify_exp=True)
        except (InvalidTokenError, ValueError) as exc:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, {'error': 'invalid_request', 'error_description': 'invalid actor_token'}) from exc

    try:
        sender_constraint = validate_sender_constraint(request, deployment, dpop_proof=dpop or dpop_proof_from_request(request))
    except OAuthPolicyViolation as exc:
        raise HTTPException(exc.status_code, {'error': exc.error, 'error_description': exc.description}) from exc
    except ValueError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, {'error': 'invalid_dpop_proof'}) from exc

    resources = data.get('resource', [])
    values = resources if isinstance(resources, list) else ([str(resources)] if resources else [])
    try:
        selection = select_resource_indicator([str(item) for item in values], audience=str(data.get('audience') or '') or None) if values else None
    except ValueError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, {'error': 'invalid_target'}) from exc

    scope = str(data.get('scope') or subject_claims.get('scope') or '') or None
    audience = (
        (selection.audience if selection is not None else None)
        or (str(data.get('audience')) if data.get('audience') not in {None, ''} else None)
        or (subject_claims.get('aud') if subject_claims.get('aud') not in {None, ''} else None)
        or settings.protected_resource_identifier
    )
    actor = _actor_claim(actor_claims)
    exchange_mode = 'delegation' if actor and actor.get('sub') != str(subject_claims.get('sub') or '') else 'impersonation'
    jwt_kwargs: Dict[str, Any] = {
        'scope': scope,
        'act': actor,
        'subject_token_type': str(subject_token_type),
        'requested_token_type': requested_token_type,
        'issuer': str(deployment.issuer or ISSUER),
        'audience': audience,
        'exchange_mode': exchange_mode,
        'source_issuer': subject_claims.get('iss'),
    }
    if sender_constraint.confirmation_claim:
        jwt_kwargs['cnf'] = sender_constraint.confirmation_claim
    access_token = await jwt.async_sign(
        sub=str(subject_claims.get('sub')),
        tid=str(subject_claims.get('tid')) if subject_claims.get('tid') is not None else None,
        cert_thumbprint=sender_constraint.cert_thumbprint,
        **jwt_kwargs,
    )
    await append_audit_event_async(
        tenant_id=None,
        actor_client_id=None,
        event_type='oauth2.token_exchange.issued',
        target_type='token',
        target_id=str(subject_claims.get('sub') or ''),
        details={
            'subject_token_type': str(subject_token_type),
            'requested_token_type': requested_token_type,
            'audience': audience,
            'resource': selection.resource if selection is not None else None,
            'resources': list(selection.resources) if selection is not None else [],
            'exchange_mode': exchange_mode,
            'actor_subject': actor.get('sub') if actor else None,
            'subject_issuer': subject_claims.get('iss'),
            'sender_constraint': sender_constraint.mechanism,
        },
    )
    response: Dict[str, Any] = {
        'access_token': access_token,
        'issued_token_type': requested_token_type,
        'token_type': sender_constraint.token_type,
    }
    if scope:
        response['scope'] = scope
    if audience:
        response['audience'] = audience
    if exchange_mode:
        response['exchange_mode'] = exchange_mode
    return response



def describe() -> dict[str, object]:
    return {
        'label': OWNER.label,
        'title': OWNER.title,
        'runtime_status': OWNER.runtime_status,
        'public_surface': list(OWNER.public_surface),
        'notes': OWNER.notes,
        'requested_token_types_supported': list(SUPPORTED_REQUESTED_TOKEN_TYPES),
        'delegation_supported': True,
        'single_effective_target': True,
        'spec_url': RFC8693_SPEC_URL,
    }



def include_token_exchange_endpoint(app: TigrblApp) -> None:
    path = '/token/exchange'
    if settings.enable_rfc8693 and not any(
        (getattr(route, 'path', None) or getattr(route, 'path_template', None)) == path
        for route in getattr(app.router, 'routes', [])
    ):
        app.include_router(api)


include_rfc8693 = include_token_exchange_endpoint


__all__ = [
    'RFC8693_SPEC_URL',
    'SUPPORTED_REQUESTED_TOKEN_TYPES',
    'TOKEN_EXCHANGE_GRANT_TYPE',
    'StandardOwner',
    'OWNER',
    'api',
    'router',
    'token_exchange',
    'describe',
    'include_token_exchange_endpoint',
    'include_rfc8693',
]
