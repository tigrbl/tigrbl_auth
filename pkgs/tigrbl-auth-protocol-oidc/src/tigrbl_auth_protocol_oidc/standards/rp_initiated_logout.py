from __future__ import annotations

"""OpenID Connect RP-Initiated Logout with durable fanout planning and replay protection."""

from dataclasses import dataclass
from datetime import datetime, timezone
import base64
import json
from typing import Any, Final
from urllib.parse import urlparse
from uuid import UUID

from tigrbl_identity_runtime.deployment import deployment_from_request, resolve_deployment
from tigrbl_identity_runtime.settings import settings

try:  # dependency-light import path for checkpoint evidence generation
    from tigrbl_identity_server.framework import HTTPException, status
except Exception:  # pragma: no cover - exercised in dependency-light tests
    class _FallbackStatus:
        HTTP_400_BAD_REQUEST = 400
        HTTP_401_UNAUTHORIZED = 401
        HTTP_404_NOT_FOUND = 404

    class HTTPException(Exception):
        def __init__(self, status_code: int, detail: Any):
            super().__init__(detail)
            self.status_code = status_code
            self.detail = detail

    status = _FallbackStatus()

STATUS: Final[str] = "rp-initiated-logout-runtime"


@dataclass(frozen=True, slots=True)
class StandardOwner:
    label: str
    title: str
    runtime_status: str
    public_surface: tuple[str, ...]
    notes: str


@dataclass(frozen=True, slots=True)
class LogoutRequestContext:
    client_id: UUID | None
    post_logout_redirect_uri: str | None
    id_token_hint_claims: dict[str, Any] | None


OWNER = StandardOwner(
    label="OIDC RP-Initiated Logout",
    title="OpenID Connect RP-Initiated Logout",
    runtime_status=STATUS,
    public_surface=("/logout",),
    notes=(
        "The canonical /logout route validates registered post-logout redirect URIs, validates id_token_hint "
        "claims against issuer/audience/session policy, persists logout fanout plans, and reuses an existing "
        "logout_state record to provide replay-safe idempotence when logout is retried."
    ),
)


def _persistence():
    from tigrbl_identity_storage import persistence as persistence_module

    return persistence_module


def _frontchannel_builder():
    from tigrbl_auth_protocol_oidc.standards.frontchannel_logout import build_frontchannel_descriptor

    return build_frontchannel_descriptor


def _backchannel_builder():
    from tigrbl_auth_protocol_oidc.standards.backchannel_logout import build_backchannel_descriptor

    return build_backchannel_descriptor


async def _verify_id_token_hint(token: str, *, issuer: str, audience: str):
    from tigrbl_auth_protocol_oidc.standards.id_token import verify_id_token

    return await verify_id_token(token, issuer=issuer, audience=audience)


def _normalized_uris(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value if item]
    if isinstance(value, str):
        return [item for item in value.split() if item]
    return [str(value)]


def _normalize_uuid(value: Any) -> UUID | None:
    if value in {None, '', False}:
        return None
    if isinstance(value, UUID):
        return value
    try:
        return UUID(str(value))
    except Exception:
        return None


def _audiences(claims: dict[str, Any] | None) -> list[str]:
    if not claims:
        return []
    aud = claims.get('aud')
    if aud is None:
        return []
    if isinstance(aud, (list, tuple, set)):
        return [str(item) for item in aud if item not in {None, ''}]
    return [str(aud)] if aud not in {None, ''} else []


def _unsafe_decode_jwt_claims(token: str) -> dict[str, Any]:
    try:
        parts = str(token).split('.')
        if len(parts) != 3:
            return {}
        padded = parts[1] + '=' * (-len(parts[1]) % 4)
        return dict(json.loads(base64.urlsafe_b64decode(padded).decode('utf-8')))
    except Exception:
        return {}


def _require_https_if_present(uri: str) -> None:
    parsed = urlparse(uri)
    if parsed.scheme != 'https':
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'post_logout_redirect_uri must use https')


def assert_logout_session_active(session_row) -> None:
    if session_row is None:
        return None
    state = str(getattr(session_row, 'session_state', 'active') or 'active').lower()
    if getattr(session_row, 'ended_at', None) is not None or state in {'terminated', 'expired', 'ended', 'revoked'}:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, {'error': 'expired_session'})


async def validate_post_logout_redirect_uri(*, client_id: UUID | None, post_logout_redirect_uri: str | None) -> str | None:
    if not post_logout_redirect_uri:
        return None
    _require_https_if_present(post_logout_redirect_uri)
    if client_id is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, {'error': 'invalid_client', 'error_description': 'client_id required when post_logout_redirect_uri is supplied'})
    registration = await _persistence().get_client_registration_async(client_id)
    metadata = dict(getattr(registration, 'registration_metadata', {}) or {})
    allowed = _normalized_uris(metadata.get('post_logout_redirect_uris'))
    if post_logout_redirect_uri not in allowed:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, {'error': 'invalid_request', 'error_description': 'unregistered post_logout_redirect_uri'})
    return post_logout_redirect_uri


async def validate_id_token_hint(
    *,
    id_token_hint: str | None,
    client_id: UUID | str | None = None,
    session_id: UUID | str | None = None,
    issuer: str | None = None,
) -> dict[str, Any] | None:
    if not id_token_hint:
        return None
    effective_issuer = issuer or settings.issuer
    effective_client_id = _normalize_uuid(client_id)
    if effective_client_id is None:
        unverified = _unsafe_decode_jwt_claims(id_token_hint)
        for audience in _audiences(unverified):
            parsed = _normalize_uuid(audience)
            if parsed is not None:
                effective_client_id = parsed
                break
    if effective_client_id is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, {'error': 'invalid_id_token_hint', 'error_description': 'unable to derive client_id from id_token_hint'})
    try:
        claims = dict(await _verify_id_token_hint(id_token_hint, issuer=effective_issuer, audience=str(effective_client_id)))
    except Exception as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, {'error': 'invalid_id_token_hint'}) from exc
    if str(claims.get('iss') or '') != effective_issuer:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, {'error': 'invalid_id_token_hint', 'error_description': 'issuer mismatch'})
    audiences = _audiences(claims)
    if str(effective_client_id) not in audiences:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, {'error': 'invalid_id_token_hint', 'error_description': 'audience mismatch'})
    expected_session_id = _normalize_uuid(session_id)
    if expected_session_id is not None:
        sid = _normalize_uuid(claims.get('sid'))
        if sid is not None and sid != expected_session_id:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, {'error': 'invalid_id_token_hint', 'error_description': 'sid mismatch'})
    return claims


def resolve_logout_client_id(*, requested_client_id: UUID | str | None, session_row=None, hint_claims: dict[str, Any] | None = None) -> UUID | None:
    requested = _normalize_uuid(requested_client_id)
    session_client = _normalize_uuid(getattr(session_row, 'client_id', None)) if session_row is not None else None
    hint_candidates = {_normalize_uuid(audience) for audience in _audiences(hint_claims)}
    hint_candidates.discard(None)

    if requested is not None and session_client is not None and requested != session_client:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, {'error': 'invalid_client', 'error_description': 'requested client does not own the session'})
    if requested is not None and hint_candidates and requested not in hint_candidates:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, {'error': 'invalid_client', 'error_description': 'requested client does not match id_token_hint'})
    if session_client is not None and hint_candidates and session_client not in hint_candidates:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, {'error': 'invalid_client', 'error_description': 'session client does not match id_token_hint'})

    if requested is not None:
        return requested
    if session_client is not None:
        return session_client
    for candidate in hint_candidates:
        return candidate
    return None


async def validate_logout_request(
    *,
    requested_client_id: UUID | str | None,
    post_logout_redirect_uri: str | None,
    id_token_hint: str | None,
    session_row=None,
    issuer: str | None = None,
) -> LogoutRequestContext:
    assert_logout_session_active(session_row)
    prevalidated_client_id = _normalize_uuid(requested_client_id) or _normalize_uuid(getattr(session_row, 'client_id', None))
    hint_claims = await validate_id_token_hint(
        id_token_hint=id_token_hint,
        client_id=prevalidated_client_id,
        session_id=getattr(session_row, 'id', None),
        issuer=issuer,
    )
    client_id = resolve_logout_client_id(requested_client_id=requested_client_id, session_row=session_row, hint_claims=hint_claims)
    redirect_uri = await validate_post_logout_redirect_uri(
        client_id=client_id,
        post_logout_redirect_uri=post_logout_redirect_uri,
    )
    return LogoutRequestContext(
        client_id=client_id,
        post_logout_redirect_uri=redirect_uri,
        id_token_hint_claims=hint_claims,
    )


async def build_logout_plan(
    *,
    session_row,
    client_id: UUID | None,
    post_logout_redirect_uri: str | None,
    state: str | None,
    reason: str = 'logout',
    metadata: dict[str, Any] | None = None,
    deployment=None,
):
    deployment = deployment if deployment is not None else resolve_deployment(settings)
    persistence = _persistence()
    now = datetime.now(timezone.utc).replace(microsecond=0)
    existing = await persistence.get_latest_logout_for_session_async(session_row.id)
    if existing is not None:
        existing_meta = dict(getattr(existing, 'logout_metadata', {}) or {})
        if post_logout_redirect_uri and 'post_logout_redirect_uri' not in existing_meta:
            existing_meta['post_logout_redirect_uri'] = post_logout_redirect_uri
        if state and 'state' not in existing_meta:
            existing_meta['state'] = state
        existing_meta['replay_count'] = int(existing_meta.get('replay_count', 0)) + 1
        existing_meta['replayed_at'] = now.isoformat()
        if metadata:
            existing_meta.update(metadata)
        if existing_meta != dict(getattr(existing, 'logout_metadata', {}) or {}):
            existing = await persistence.update_logout_metadata_async(existing.id, metadata=existing_meta) or existing
        return existing

    front_required = bool(client_id and deployment.flag_enabled('enable_oidc_frontchannel_logout'))
    back_required = bool(client_id and deployment.flag_enabled('enable_oidc_backchannel_logout'))
    combined_meta = {
        'post_logout_redirect_uri': post_logout_redirect_uri,
        'state': state,
        'client_id': str(client_id) if client_id is not None else None,
        'request_validated_at': now.isoformat(),
        'replay_count': 0,
        'frontchannel_delivery': {'status': 'pending' if front_required else 'not_configured', 'attempts': 0, 'max_retries': 3},
        'backchannel_delivery': {'status': 'pending' if back_required else 'not_configured', 'attempts': 0, 'max_retries': 3},
    }
    if metadata:
        combined_meta.update(metadata)
    logout = await persistence.terminate_session_async(
        session_row.id,
        initiated_by='rp_logout',
        reason=reason,
        frontchannel_required=front_required,
        backchannel_required=back_required,
        metadata=combined_meta,
    )
    if logout is None:
        return None

    frontchannel = None
    backchannel = None
    if client_id is not None:
        frontchannel = await _frontchannel_builder()(
            client_id=client_id,
            sid=str(session_row.id),
            iss=str(deployment.issuer or settings.issuer),
            logout_id=logout.id,
        )
        backchannel = await _backchannel_builder()(
            client_id=client_id,
            sid=str(session_row.id),
            sub=str(session_row.user_id),
            iss=str(deployment.issuer or settings.issuer),
            logout_id=logout.id,
        )
    plan_meta = dict(logout.logout_metadata or {})
    plan_meta.update({
        'post_logout_redirect_uri': post_logout_redirect_uri,
        'state': state,
        'frontchannel': frontchannel,
        'backchannel': backchannel,
        'frontchannel_delivery': (frontchannel or {}).get('delivery') if isinstance(frontchannel, dict) else {'status': 'not_configured', 'attempts': 0, 'max_retries': 3},
        'backchannel_delivery': (backchannel or {}).get('delivery') if isinstance(backchannel, dict) else {'status': 'not_configured', 'attempts': 0, 'max_retries': 3},
        'idempotent_replay_protection': True,
        'replay_count': 0,
    })
    return await persistence.update_logout_metadata_async(logout.id, metadata=plan_meta) or logout


def describe(*, request=None, deployment=None) -> dict[str, object]:
    if deployment is None and request is not None:
        deployment = deployment_from_request(request, settings)
    return {
        'label': OWNER.label,
        'title': OWNER.title,
        'runtime_status': OWNER.runtime_status,
        'public_surface': list(OWNER.public_surface),
        'id_token_hint_validation_supported': True,
        'post_logout_redirect_uri_validation_supported': True,
        'idempotent_replay_protection': True,
        'frontchannel_logout_supported': bool(getattr(deployment, "flag_enabled", lambda *_: True)("enable_oidc_frontchannel_logout")) if deployment is not None else True,
        'backchannel_logout_supported': bool(getattr(deployment, "flag_enabled", lambda *_: True)("enable_oidc_backchannel_logout")) if deployment is not None else True,
        'notes': OWNER.notes,
    }


__all__ = [
    'STATUS',
    'LogoutRequestContext',
    'StandardOwner',
    'OWNER',
    'assert_logout_session_active',
    'build_logout_plan',
    'describe',
    'resolve_logout_client_id',
    'validate_id_token_hint',
    'validate_logout_request',
    'validate_post_logout_redirect_uri',
]
