from __future__ import annotations

"""Rich Authorization Requests owner and helper module."""

import json
from dataclasses import dataclass
from typing import Any, Final
from urllib.parse import urlparse

from tigrbl_auth.config.settings import settings
from tigrbl_auth.standards.oauth2.resource_indicators import select_resource_indicator

try:  # pragma: no cover - exercised when the full runtime stack is installed
    from tigrbl_auth.framework import BaseModel, ValidationError
except Exception:  # pragma: no cover - dependency-light fallback for checkpoint tests/evidence
    from pydantic import BaseModel, ValidationError  # type: ignore

STATUS: Final[str] = 'rich-authorization-runtime'
RFC9396_SPEC_URL: Final[str] = 'https://www.rfc-editor.org/rfc/rfc9396'


@dataclass(frozen=True, slots=True)
class StandardOwner:
    label: str
    title: str
    runtime_status: str
    public_surface: tuple[str, ...]
    notes: str


@dataclass(frozen=True, slots=True)
class AuthorizationDetailsBinding:
    details: list[dict[str, Any]]
    resource: str | None
    audience: str | None


OWNER = StandardOwner(
    label='RFC 9396',
    title='OAuth 2.0 Rich Authorization Requests',
    runtime_status=STATUS,
    public_surface=('/authorize', '/par'),
    notes=(
        'Canonical standards-tree owner module for authorization_details parsing, validation, '
        'resource coupling, and propagation into authorization and PAR handling.'
    ),
)


class AuthorizationDetail(BaseModel):
    type: str
    actions: list[str] | None = None
    locations: list[str] | None = None
    datatypes: list[str] | None = None
    identifier: str | None = None
    privileges: list[str] | None = None
    resource: str | None = None
    resource_indicator: str | None = None

    model_config = {'extra': 'allow'}



def _is_absolute_uri(value: str) -> bool:
    parsed = urlparse(value)
    return bool(parsed.scheme and parsed.netloc and not parsed.fragment)



def _normalize_locations(value: Any) -> list[str] | None:
    if value is None or value == '':
        return None
    if isinstance(value, str):
        items = [value]
    elif isinstance(value, (list, tuple, set)):
        items = [str(item) for item in value if str(item)]
    else:
        raise ValueError(f'authorization_details locations must be a string or array: {RFC9396_SPEC_URL}')
    normalized = []
    for item in items:
        if not _is_absolute_uri(item):
            raise ValueError(f'authorization_details locations must be absolute URIs: {RFC9396_SPEC_URL}')
        normalized.append(item)
    return normalized or None



def _normalize_multi_string(name: str, value: Any) -> list[str] | None:
    if value is None or value == '':
        return None
    if isinstance(value, str):
        items = [value]
    elif isinstance(value, (list, tuple, set)):
        items = [str(item) for item in value if str(item)]
    else:
        raise ValueError(f'authorization_details {name} must be a string or array: {RFC9396_SPEC_URL}')
    return items or None



def _normalize_detail(detail: AuthorizationDetail) -> dict[str, Any]:
    payload = detail.model_dump(exclude_none=True)
    payload['type'] = str(payload['type'])
    if not payload['type']:
        raise ValueError(f'authorization_details.type is required: {RFC9396_SPEC_URL}')
    if 'locations' in payload:
        payload['locations'] = _normalize_locations(payload.get('locations'))
        if payload['locations'] is None:
            payload.pop('locations', None)
    for key in ('actions', 'datatypes', 'privileges'):
        if key in payload:
            payload[key] = _normalize_multi_string(key, payload.get(key))
            if payload[key] is None:
                payload.pop(key, None)
    for key in ('resource', 'resource_indicator'):
        if key in payload and payload[key] not in {None, ''}:
            value = str(payload[key])
            if not _is_absolute_uri(value):
                raise ValueError(f'authorization_details {key} must be an absolute URI: {RFC9396_SPEC_URL}')
            payload[key] = value
        else:
            payload.pop(key, None)
    return payload



def parse_authorization_details(raw: str) -> list[AuthorizationDetail]:
    if not settings.enable_rfc9396:
        raise NotImplementedError(f'authorization_details not enabled: {RFC9396_SPEC_URL}')
    try:
        data: Any = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f'authorization_details must be valid JSON: {RFC9396_SPEC_URL}') from exc
    if isinstance(data, dict):
        data = [data]
    if not isinstance(data, list):
        raise ValueError(f'authorization_details must be an object or array: {RFC9396_SPEC_URL}')
    try:
        return [AuthorizationDetail.model_validate(item) for item in data]
    except ValidationError as exc:
        raise ValueError(f'invalid authorization_details: {RFC9396_SPEC_URL}') from exc



def bind_authorization_details(
    details: list[AuthorizationDetail] | list[dict[str, Any]],
    *,
    resource: str | None = None,
    audience: str | None = None,
) -> AuthorizationDetailsBinding:
    if not settings.enable_rfc9396:
        raise NotImplementedError(f'authorization_details not enabled: {RFC9396_SPEC_URL}')
    bound_details: list[dict[str, Any]] = []
    effective_target = audience or resource
    for item in details:
        detail = item if isinstance(item, AuthorizationDetail) else AuthorizationDetail.model_validate(item)
        payload = _normalize_detail(detail)
        detail_targets: list[str] = []
        if payload.get('resource'):
            detail_targets.append(str(payload['resource']))
        if payload.get('resource_indicator'):
            detail_targets.append(str(payload['resource_indicator']))
        if payload.get('locations'):
            detail_targets.extend([str(location) for location in payload['locations']])
        if detail_targets:
            try:
                selection = select_resource_indicator(detail_targets, audience=effective_target)
            except ValueError as exc:
                raise ValueError(f'authorization_details resource binding is inconsistent: {RFC9396_SPEC_URL}') from exc
            effective_target = selection.audience or effective_target
            payload['_resource'] = selection.resource
        elif effective_target:
            payload['_resource'] = effective_target
        bound_details.append(payload)
    return AuthorizationDetailsBinding(details=bound_details, resource=effective_target, audience=effective_target)



def normalize_authorization_details(raw: str | list[dict[str, Any]] | dict[str, Any], *, resource: str | None = None, audience: str | None = None) -> AuthorizationDetailsBinding:
    if isinstance(raw, str):
        details = parse_authorization_details(raw)
    else:
        payload = raw if isinstance(raw, list) else [raw]
        details = [AuthorizationDetail.model_validate(item) for item in payload]
    return bind_authorization_details(details, resource=resource, audience=audience)



def describe() -> dict[str, object]:
    return {
        'label': OWNER.label,
        'title': OWNER.title,
        'runtime_status': OWNER.runtime_status,
        'public_surface': list(OWNER.public_surface),
        'notes': OWNER.notes,
        'spec_url': RFC9396_SPEC_URL,
    }


__all__ = [
    'STATUS',
    'RFC9396_SPEC_URL',
    'StandardOwner',
    'AuthorizationDetail',
    'AuthorizationDetailsBinding',
    'OWNER',
    'parse_authorization_details',
    'bind_authorization_details',
    'normalize_authorization_details',
    'describe',
]
