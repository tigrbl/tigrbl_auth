from __future__ import annotations

"""Resource Indicators for OAuth 2.0 owner and helper module.

The repository retains a bounded but certification-grade resource-indicator
profile:

- every supplied ``resource`` value must be a valid absolute URI
- multiple identical values are allowed
- multiple *distinct* values fail closed with ``invalid_target`` in the active
  release path because this package binds one effective resource audience per
  request/issued token
- when both ``audience`` and ``resource`` are supplied they must resolve to the
  same effective target or the request fails closed with ``invalid_target``
"""

from dataclasses import dataclass
from typing import Final, Iterable, Sequence
from tigrbl_identity_core.standards import StandardOwner, describe_owner
from urllib.parse import urlparse

STATUS: Final[str] = 'resource-bound-runtime'
RFC8707_SPEC_URL: Final[str] = 'https://www.rfc-editor.org/rfc/rfc8707'




OWNER = StandardOwner(
    label='RFC 8707',
    title='Resource Indicators for OAuth 2.0',
    runtime_status=STATUS,
    public_surface=('/authorize', '/token', '/device_authorization', '/token/exchange', '/par'),
    notes=(
        'Canonical standards-tree owner module for resource indicator validation across '
        'authorization, token, PAR, device, and token-exchange surfaces. The active '
        'release path binds one effective resource audience per request and fails '
        'closed on conflicting or ambiguous resource/audience inputs.'
    ),
)


@dataclass(frozen=True, slots=True)
class ResourceSelection:
    resources: tuple[str, ...]
    resource: str | None
    audience: str | None



def _coerce_resources(resources: Sequence[str] | str | None) -> list[str]:
    if resources is None:
        return []
    if isinstance(resources, str):
        return [resources] if resources else []
    if isinstance(resources, Sequence) and len(resources) == 0:
        return []
    return [str(item) for item in resources if str(item)]



def _validate_resource_uri(value: str) -> str:
    parsed = urlparse(value)
    if not parsed.scheme or not parsed.netloc or parsed.fragment:
        raise ValueError(f'invalid resource indicator: {RFC8707_SPEC_URL}')
    return value



def select_resource_indicator(
    resources: Sequence[str] | str | None,
    *,
    audience: str | None = None,
    allow_multiple_distinct: bool = False,
) -> ResourceSelection:
    normalized = [_validate_resource_uri(item) for item in _coerce_resources(resources)]
    distinct = tuple(dict.fromkeys(normalized))
    if not distinct:
        return ResourceSelection(resources=(), resource=None, audience=audience)
    if len(distinct) > 1 and not allow_multiple_distinct:
        raise ValueError(f'ambiguous resource indicators are not supported: {RFC8707_SPEC_URL}')
    selected = distinct[0]
    if audience not in {None, '', selected}:
        raise ValueError(f'conflicting audience/resource values are not supported: {RFC8707_SPEC_URL}')
    return ResourceSelection(resources=distinct, resource=selected, audience=selected if selected is not None else audience)



def extract_resource(resources: Sequence[str] | str | None, *, audience: str | None = None) -> str | None:
    return select_resource_indicator(resources, audience=audience).resource



def resource_binding_summary(resources: Sequence[str] | str | None, *, audience: str | None = None) -> dict[str, object]:
    selection = select_resource_indicator(resources, audience=audience)
    return {
        'resource_count': len(selection.resources),
        'resources': list(selection.resources),
        'resource': selection.resource,
        'audience': selection.audience,
        'single_effective_target': True,
    }



def describe() -> dict[str, object]:
    return describe_owner(
        OWNER,
        single_effective_target=True,
        conflicting_inputs_fail_closed=True,
        spec_url=RFC8707_SPEC_URL,
    )


__all__ = [
    'STATUS',
    'RFC8707_SPEC_URL',
    'StandardOwner',
    'OWNER',
    'ResourceSelection',
    'extract_resource',
    'resource_binding_summary',
    'select_resource_indicator',
    'describe',
]
