from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs
from uuid import UUID

from tigrbl_identity_runtime.deployment import deployment_from_app, deployment_from_request
from tigrbl_identity_runtime.settings import settings
from .ops.common import create_record, read_record
from tigrbl_identity_storage.tables.audit_event import AuditEvent

try:  # pragma: no cover - exercised with full runtime deps installed
    from tigrbl_identity_storage.framework import Depends, HTTPException, TigrblApp, TigrblRouter, status
    from tigrbl_identity_storage.tables.engine import get_db
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
    def Depends(dependency):
        return dependency  # type: ignore[assignment]

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

from tigrbl_auth_protocol_oauth.standards.device_authorization import (
    DEVICE_CODE_EXPIRES_IN,
    DEVICE_CODE_INTERVAL,
    generate_device_code,
    generate_user_code,
)
from tigrbl_auth_protocol_oauth.standards.resource_indicators import select_resource_indicator

try:  # pragma: no cover
    from tigrbl_identity_storage.tables.client import Client
    from tigrbl_identity_storage.tables.device_code import DeviceAuthorizationOut, DeviceCode
except Exception:  # pragma: no cover - placeholders for dependency-light tests
    class Client:  # type: ignore[override]
        id = object()

    class DeviceCode:  # type: ignore[override]
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
            self.id = kwargs.get('id') or kwargs.get('device_code')

    class DeviceAuthorizationOut:  # type: ignore[override]
        pass


api = router = TigrblRouter()


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
    client = await read_record(Client, db, client_uuid)
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
    row = await create_record(
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

    await create_record(
        AuditEvent,
        db,
        {
            'tenant_id': client.tenant_id,
            'actor_client_id': client.id,
            'event_type': 'device.authorization.created',
            'target_type': 'device_code',
            'target_id': str(getattr(row, 'id', device_code)),
            'details': {
                'audience': effective_audience,
                'resource': effective_resource,
                'resources': list(selection.resources) if selection is not None else [],
                'scope': scope,
                'interval': DEVICE_CODE_INTERVAL,
                'expires_in': DEVICE_CODE_EXPIRES_IN,
                'user_code_length': len(user_code),
                'user_code_charset': 'A-Z0-9',
            },
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


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[5]


@api.route("/device_authorization", methods=["POST"], response_model=DeviceAuthorizationOut)
async def device_authorization(request: Any, db: Any = Depends(get_db)) -> Any:
    result = await device_authorization_request(request=request, db=db)
    from tigrbl_identity_storage_runtime.session_service import observe_device_authorization_response

    payload = result if isinstance(result, dict) else getattr(result, "model_dump", lambda **_: {})(mode="json")
    observe_device_authorization_response(_repo_root(), device_code=payload.get("device_code"), details=payload)
    return result


def include_device_authorization_endpoint(app: TigrblApp) -> None:
    deployment = deployment_from_app(app, settings)
    path = "/device_authorization"
    if deployment.route_enabled(path) and not any(
        (getattr(route, "path", None) or getattr(route, "path_template", None)) == path
        for route in app.router.routes
    ):
        app.include_router(api)


include_rfc8628 = include_device_authorization_endpoint


__all__ = [
    "api",
    "router",
    "device_authorization",
    "device_authorization_request",
    "include_device_authorization_endpoint",
    "include_rfc8628",
]
