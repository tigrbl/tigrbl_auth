"""OAuth 2.0 Pushed Authorization Requests owner and helper module."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Final, Mapping

from tigrbl_identity_contracts.oauth import (
    PARValidationResult,
    PushedAuthorizationPersistenceRequest,
    PushedAuthorizationResult,
)
from tigrbl_identity_core.standards import StandardOwner, describe_owner
from tigrbl_pushed_authorization_capability import PushedAuthorizationCapability

STATUS: Final[str] = 'durable-request-uri-runtime'
RFC9126_SPEC_URL: Final[str] = 'https://www.rfc-editor.org/rfc/rfc9126'
REQUEST_URI_PREFIX: Final[str] = 'urn:ietf:params:oauth:request_uri:'
PAR_ONE_TIME_USE: Final[bool] = True




OWNER = StandardOwner(
    label='RFC 9126',
    title='OAuth 2.0 Pushed Authorization Requests',
    runtime_status=STATUS,
    public_surface=('/par', '/authorize'),
    notes=(
        'Authoritative standards-tree owner module for durable PAR persistence, request_uri '
        'validation, expiration checks, client binding, and one-time consumption semantics.'
    ),
)


class PushedAuthorizationRequestError(ValueError):
    """Raised when a pushed authorization request violates the active PAR policy."""


class PushedAuthorizationDisabledError(RuntimeError):
    """Raised when composition disables the RFC 9126 protocol feature."""


@dataclass(frozen=True, slots=True)
class RFC9126PushedAuthorizationService:
    """Map normalized RFC 9126 input to durable pushed authorization."""

    capability: PushedAuthorizationCapability
    enabled: bool = True

    async def push(
        self,
        *,
        client_id: str,
        tenant_id: str | None,
        params: Mapping[str, object],
    ) -> PushedAuthorizationResult:
        if not self.enabled:
            raise PushedAuthorizationDisabledError(
                f"RFC 9126 support is disabled: {RFC9126_SPEC_URL}"
            )
        call = await self.capability.call(
            "push_authorization_request",
            PushedAuthorizationPersistenceRequest(
                client_id=client_id,
                tenant_id=tenant_id,
                params=dict(params),
            ),
        )
        result = call.value
        if not isinstance(result, PushedAuthorizationResult):
            raise TypeError(
                "oauth.pushed-authorization must return PushedAuthorizationResult"
            )
        validate_request_uri(result.request_uri)
        return result



def _utc(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value if value.tzinfo is not None else value.replace(tzinfo=timezone.utc)
    raise PushedAuthorizationRequestError(f'invalid PAR timestamp value: {RFC9126_SPEC_URL}')



def is_request_uri(value: str | None) -> bool:
    return bool(value) and str(value).startswith(REQUEST_URI_PREFIX)



def validate_request_uri(value: str | None) -> str:
    request_uri = str(value or '').strip()
    if not is_request_uri(request_uri):
        raise PushedAuthorizationRequestError(f'invalid request_uri value: {RFC9126_SPEC_URL}')
    return request_uri



def validate_pushed_authorization_request_row(
    row: Any,
    *,
    client_id: str | None = None,
    request_uri: str | None = None,
    now: datetime | None = None,
) -> PARValidationResult:
    effective_request_uri = validate_request_uri(request_uri or getattr(row, 'request_uri', None))
    row_request_uri = validate_request_uri(getattr(row, 'request_uri', None))
    if row_request_uri != effective_request_uri:
        raise PushedAuthorizationRequestError(f'request_uri mismatch: {RFC9126_SPEC_URL}')
    expires_at = _utc(getattr(row, 'expires_at', None))
    current = now if now is not None else datetime.now(timezone.utc)
    current = current if current.tzinfo is not None else current.replace(tzinfo=timezone.utc)
    consumed_at = getattr(row, 'consumed_at', None)
    if consumed_at is not None:
        consumed_at = _utc(consumed_at)
    if expires_at <= current:
        raise PushedAuthorizationRequestError(f'request_uri has expired: {RFC9126_SPEC_URL}')
    if PAR_ONE_TIME_USE and consumed_at is not None:
        raise PushedAuthorizationRequestError(f'request_uri has already been consumed: {RFC9126_SPEC_URL}')
    bound_client = getattr(row, 'client_id', None)
    if client_id not in {None, ''} and bound_client not in {None, '', client_id} and str(bound_client) != str(client_id):
        raise PushedAuthorizationRequestError(f'request_uri is not bound to the presented client_id: {RFC9126_SPEC_URL}')
    params = dict(getattr(row, 'params', None) or {})
    return PARValidationResult(
        request_uri=row_request_uri,
        client_id=str(bound_client) if bound_client not in {None, ''} else None,
        expires_at=expires_at,
        consumed=consumed_at is not None,
        params=params,
    )



def consume_pushed_authorization_request(row: Any, *, now: datetime | None = None) -> datetime:
    consumed_at = now if now is not None else datetime.now(timezone.utc)
    consumed_at = consumed_at if consumed_at.tzinfo is not None else consumed_at.replace(tzinfo=timezone.utc)
    setattr(row, 'consumed_at', consumed_at)
    return consumed_at



def par_result_payload(result: PARValidationResult) -> dict[str, Any]:
    return {
        'request_uri': result.request_uri,
        'client_id': result.client_id,
        'expires_at': result.expires_at.isoformat(),
        'consumed': result.consumed,
        'param_keys': sorted(result.params.keys()),
    }



def describe() -> dict[str, object]:
    return describe_owner(
        OWNER,
        request_uri_prefix=REQUEST_URI_PREFIX,
        one_time_use=PAR_ONE_TIME_USE,
        spec_url=RFC9126_SPEC_URL,
    )


__all__ = [
    'STATUS',
    'RFC9126_SPEC_URL',
    'REQUEST_URI_PREFIX',
    'PAR_ONE_TIME_USE',
    'StandardOwner',
    'PARValidationResult',
    'PushedAuthorizationRequestError',
    'PushedAuthorizationDisabledError',
    'RFC9126PushedAuthorizationService',
    'OWNER',
    'is_request_uri',
    'validate_request_uri',
    'validate_pushed_authorization_request_row',
    'consume_pushed_authorization_request',
    'par_result_payload',
    'describe',
]
