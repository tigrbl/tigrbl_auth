'Device authorization grant execution.'
from __future__ import annotations

from .token_runtime import (
    Any, DEVICE_CODE_EXPIRES_IN, DeviceCode, JSONResponse,
    _json_error, _jwt, _token_pair_payload, append_audit_event_record,
    datetime, first_handler_record, issue_token_pair_records, next_device_poll_interval,
    poll_too_frequently, status, timezone, update_handler_record,
)

async def handle_device_code_grant(
    *,
    db: Any,
    data: dict[str, str],
    client: Any,
    sender_constraint: Any,
    request_audience: str | None,
    resource: str | None,
    jwt_kwargs: Any,
) -> Any:
    device_code = data.get('device_code')
    if not device_code:
        return JSONResponse({'error': 'invalid_request'}, status_code=status.HTTP_400_BAD_REQUEST)
    row = await first_handler_record(DeviceCode, db, {"device_code": device_code})
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
        await update_handler_record(
            DeviceCode,
            db,
            row.id,
            {
                'poll_count': row.poll_count,
                'slow_down_count': row.slow_down_count,
                'last_polled_at': row.last_polled_at,
                'interval': row.interval,
            },
        )
        await append_audit_event_record(
            db,
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
        await update_handler_record(DeviceCode, db, row.id, {'poll_count': row.poll_count, 'last_polled_at': row.last_polled_at})
        return _json_error('access_denied', status_code=status.HTTP_400_BAD_REQUEST)
    if not getattr(row, 'authorized', False) or getattr(row, 'user_id', None) is None or getattr(row, 'tenant_id', None) is None:
        await update_handler_record(DeviceCode, db, row.id, {'poll_count': row.poll_count, 'last_polled_at': row.last_polled_at})
        await append_audit_event_record(
            db,
            tenant_id=getattr(row, 'tenant_id', None),
            actor_client_id=getattr(row, 'client_id', None),
            event_type='device.authorization.poll.pending',
            target_type='device_code',
            target_id=str(getattr(row, 'id', device_code)),
            details={'poll_count': row.poll_count, 'expires_in': DEVICE_CODE_EXPIRES_IN},
        )
        return _json_error('authorization_pending', status_code=status.HTTP_400_BAD_REQUEST)
    effective_audience = request_audience or getattr(row, 'audience', None) or getattr(row, 'resource', None)
    access, refresh = await issue_token_pair_records(
        db,
        jwt=_jwt,
        sub=str(row.user_id),
        tid=str(row.tenant_id),
        client_id=str(client.id),
        cert_thumbprint=sender_constraint.cert_thumbprint,
        **jwt_kwargs(scope=row.scope, audience=effective_audience),
    )
    row.consumed_at = now
    await update_handler_record(
        DeviceCode,
        db,
        row.id,
        {'poll_count': row.poll_count, 'last_polled_at': row.last_polled_at, 'consumed_at': row.consumed_at},
    )
    await append_audit_event_record(
        db,
        tenant_id=getattr(row, 'tenant_id', None),
        actor_client_id=getattr(row, 'client_id', None),
        event_type='device.authorization.token_issued',
        target_type='device_code',
        target_id=str(getattr(row, 'id', device_code)),
        details={
            'poll_count': row.poll_count,
            'audience': effective_audience,
            'resource': resource,
            'interval': getattr(row, 'interval', DEVICE_CODE_INTERVAL),
        },
    )
    return _token_pair_payload(access, refresh, token_type=sender_constraint.token_type)

