from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any
from urllib.parse import parse_qs
from uuid import UUID

from tigrbl_auth.config.deployment import deployment_from_request
from tigrbl_auth.config.settings import settings
from tigrbl_auth.security.handler_records import append_audit_event_record, create_handler_record, read_handler_record

try:  # pragma: no cover - exercised with full runtime deps installed
    from tigrbl_auth.framework import HTTPException, status
except Exception:  # pragma: no cover - dependency-light fallback
    class _FallbackStatus:
        HTTP_400_BAD_REQUEST = 400
        HTTP_404_NOT_FOUND = 404

    class HTTPException(Exception):
        def __init__(self, status_code: int, detail: Any):
            super().__init__(detail)
            self.status_code = status_code
            self.detail = detail

    status = _FallbackStatus()

from tigrbl_auth.standards.oauth2.device_authorization import (
    DEVICE_CODE_EXPIRES_IN,
    DEVICE_CODE_INTERVAL,
    generate_device_code,
    generate_user_code,
)
from tigrbl_auth.standards.oauth2.resource_indicators import select_resource_indicator

try:  # pragma: no cover
    from tigrbl_auth.tables import Client, DeviceCode
except Exception:  # pragma: no cover - placeholders for dependency-light tests
    class Client:  # type: ignore[override]
        id = object()

    class DeviceCode:  # type: ignore[override]
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
            self.id = kwargs.get('id') or kwargs.get('device_code')


async def device_authorization_request(*, request, db):
    deployment = deployment_from_request(request, settings)
    if not deployment.flag_enabled('enable_rfc8628'):
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'device authorization disabled')
    body = getattr(request, 'body', b'') or b''
    form_data = parse_qs(body.decode('utf-8'), keep_blank_values=True)
    client_id = (form_data.get('client_id') or [None])[0]
    scope = (form_data.get('scope') or [None])[0]
    audience = (form_data.get('audience') or [None])[0]
    resources = [item for item in form_data.get('resource', []) if item]

    if not client_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'client_id parameter required')
    try:
        client_uuid = UUID(str(client_id))
    except Exception as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'invalid client_id') from exc
    client = await read_handler_record(Client, db, client_uuid)
    if client is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'client not found')

    selection = None
    if resources:
        if not deployment.flag_enabled('enable_rfc8707'):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, 'resource indicators disabled')
        try:
            selection = select_resource_indicator(resources, audience=audience)
        except ValueError as exc:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, 'invalid_target') from exc
    effective_resource = selection.resource if selection is not None else None
    effective_audience = selection.audience if selection is not None else audience

    device_code = generate_device_code()
    user_code = generate_user_code()
    expires_at = datetime.now(timezone.utc) + timedelta(seconds=DEVICE_CODE_EXPIRES_IN)
    row = await create_handler_record(
        DeviceCode,
        db,
        {
            "device_code": device_code,
            "user_code": user_code,
            "client_id": client.id,
            "scope": scope,
            "audience": effective_audience,
            "resource": effective_resource,
            "expires_at": expires_at,
            "interval": DEVICE_CODE_INTERVAL,
            "poll_count": 0,
            "slow_down_count": 0,
            "tenant_id": client.tenant_id,
        },
    )

    verification_uri = f"{str(deployment.issuer or settings.issuer).rstrip('/')}/device"
    verification_uri_complete = f"{verification_uri}?user_code={user_code}"

    await append_audit_event_record(
        db,
        tenant_id=client.tenant_id,
        actor_client_id=client.id,
        event_type='device.authorization.created',
        target_type='device_code',
        target_id=str(getattr(row, 'id', device_code)),
        details={
            'audience': effective_audience,
            'resource': effective_resource,
            'resources': list(selection.resources) if selection is not None else [],
            'scope': scope,
            'interval': DEVICE_CODE_INTERVAL,
            'expires_in': DEVICE_CODE_EXPIRES_IN,
            'user_code_length': len(user_code),
            'user_code_charset': 'A-Z0-9',
        },
    )

    return {
        'device_code': device_code,
        'user_code': user_code,
        'verification_uri': verification_uri,
        'verification_uri_complete': verification_uri_complete,
        'expires_in': DEVICE_CODE_EXPIRES_IN,
        'interval': DEVICE_CODE_INTERVAL,
    }
