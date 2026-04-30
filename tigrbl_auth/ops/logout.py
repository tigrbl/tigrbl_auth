from __future__ import annotations

import json
from urllib.parse import parse_qs
from uuid import UUID

from tigrbl_auth.config.deployment import deployment_from_request
from tigrbl_auth.config.settings import settings
from tigrbl_auth.framework import HTTPException, JSONResponse, RedirectResponse, status
from tigrbl_auth.services.persistence import append_audit_event_async, get_session_async
from tigrbl_auth.standards.http.cookies import clear_session_cookie, describe_runtime_policy, parse_session_cookie_value
from tigrbl_auth.standards.oidc.rp_initiated_logout import build_logout_plan, validate_logout_request
from tigrbl_auth.standards.oidc.session_mgmt import resolve_browser_session


def _append_state(uri: str, state: str | None) -> str:
    if not state:
        return uri
    joiner = '&' if '?' in uri else '?'
    return f"{uri}{joiner}state={state}"


def _query_params(request) -> dict[str, str]:
    params = getattr(request, 'query_params', None)
    if params is None:
        return {}
    if hasattr(params, 'items'):
        return {str(k): str(v) for k, v in params.items()}
    return dict(params)


def _body_params(body: bytes) -> dict[str, str]:
    if not body:
        return {}
    text = body.decode('utf-8')
    try:
        parsed_json = json.loads(text)
        if isinstance(parsed_json, dict):
            return {str(k): str(v) for k, v in parsed_json.items() if v is not None}
    except Exception:
        pass
    parsed = parse_qs(text, keep_blank_values=True)
    return {k: v[-1] for k, v in parsed.items() if v}


def _cookie_session_id(request) -> UUID | None:
    try:
        cookie_value = (getattr(request, 'cookies', None) or {}).get(settings.session_cookie_name)
        parsed = parse_session_cookie_value(cookie_value)
        return parsed.session_id if parsed is not None else None
    except Exception:
        return None


async def logout_request(*, request, db):
    deployment = deployment_from_request(request, settings)
    if not deployment.flag_enabled('enable_oidc_rp_initiated_logout'):
        return JSONResponse({'error': 'logout disabled'}, status_code=status.HTTP_404_NOT_FOUND)

    params = _query_params(request)
    if not params:
        body = getattr(request, 'body', b'') or b''
        params = _body_params(body)

    session = await resolve_browser_session(request)
    if session is None and params.get('sid'):
        try:
            session = await get_session_async(UUID(str(params['sid'])))
        except Exception:
            session = None
    if session is None:
        cookie_session_id = _cookie_session_id(request)
        if cookie_session_id is not None:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, {'error': 'invalid_session_cookie'})

    context = await validate_logout_request(
        requested_client_id=params.get('client_id'),
        post_logout_redirect_uri=params.get('post_logout_redirect_uri'),
        id_token_hint=params.get('id_token_hint'),
        session_row=session,
        issuer=settings.issuer,
    )
    client_id = context.client_id
    redirect_uri = context.post_logout_redirect_uri
    hint_claims = context.id_token_hint_claims or {}

    logout_record = None
    if session is not None:
        logout_record = await build_logout_plan(
            session_row=session,
            client_id=client_id,
            post_logout_redirect_uri=redirect_uri,
            state=params.get('state'),
            reason='logout',
            metadata={
                'id_token_hint_present': bool(params.get('id_token_hint')),
                'id_token_hint_sid': hint_claims.get('sid'),
                'id_token_hint_sub': hint_claims.get('sub'),
            },
        )
        await append_audit_event_async(
            tenant_id=session.tenant_id,
            actor_user_id=session.user_id,
            actor_client_id=client_id,
            session_id=session.id,
            event_type='session.logout',
            target_type='session',
            target_id=str(session.id),
            details={
                'logout_id': str(getattr(logout_record, 'id', '')) if logout_record is not None else None,
                'frontchannel_required': bool(getattr(logout_record, 'frontchannel_required', False)) if logout_record is not None else False,
                'backchannel_required': bool(getattr(logout_record, 'backchannel_required', False)) if logout_record is not None else False,
            },
        )

    metadata = dict(getattr(logout_record, 'logout_metadata', {}) or {}) if logout_record is not None else {}
    payload = {
        'status': 'logged_out' if session is not None else 'no_active_session',
        'session_id': str(session.id) if session is not None else None,
        'logout_id': str(getattr(logout_record, 'id', '')) if logout_record is not None else None,
        'post_logout_redirect_uri': redirect_uri,
        'state': params.get('state'),
        'cookie_cleared': True,
        'cookie_policy': describe_runtime_policy(),
        'frontchannel_logout': metadata.get('frontchannel'),
        'backchannel_logout': metadata.get('backchannel'),
        'frontchannel_delivery': metadata.get('frontchannel_delivery'),
        'backchannel_delivery': metadata.get('backchannel_delivery'),
        'replay_protected': bool(metadata.get('idempotent_replay_protection')),
    }
    if redirect_uri:
        response = RedirectResponse(_append_state(redirect_uri, params.get('state')))
    else:
        response = JSONResponse(payload)
    response.headers['x-tigrbl-auth-logout-status'] = str(payload['status'])
    if payload.get('logout_id'):
        response.headers['x-tigrbl-auth-logout-id'] = str(payload['logout_id'])
    if payload.get('session_id'):
        response.headers['x-tigrbl-auth-session-id'] = str(payload['session_id'])
    clear_session_cookie(response)
    return response
