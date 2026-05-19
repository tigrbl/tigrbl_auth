from __future__ import annotations

"""OAuth 2.0 Dynamic Client Registration Management Protocol owner module."""

from dataclasses import dataclass
from typing import Final

STATUS: Final[str] = 'persistence-backed-client-management-runtime'
RFC7592_SPEC_URL: Final[str] = 'https://www.rfc-editor.org/rfc/rfc7592'


@dataclass(frozen=True, slots=True)
class StandardOwner:
    label: str
    title: str
    runtime_status: str
    public_surface: tuple[str, ...]
    notes: str


OWNER = StandardOwner(
    label='RFC 7592',
    title='OAuth 2.0 Dynamic Client Registration Management Protocol',
    runtime_status=STATUS,
    public_surface=('/register/{client_id}',),
    notes='Authoritative standards-tree owner module. Registration management is mounted on the public release path with bearer-authenticated GET/PUT/DELETE semantics, durable client-registration metadata persistence, and audit-observable update/delete behavior.',
)


def describe() -> dict[str, object]:
    return {
        'label': OWNER.label,
        'title': OWNER.title,
        'runtime_status': OWNER.runtime_status,
        'public_surface': list(OWNER.public_surface),
        'notes': OWNER.notes,
        'spec_url': RFC7592_SPEC_URL,
    }


__all__ = ['STATUS', 'RFC7592_SPEC_URL', 'StandardOwner', 'OWNER', 'describe']
