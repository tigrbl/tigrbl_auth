"""OIDC session service contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Mapping, Protocol


@dataclass(frozen=True, slots=True)
class SessionCreateRequest:
    subject: str
    tenant_id: str
    client_id: str | None = None
    authenticated_at: datetime | None = None
    expires_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class SessionRecord:
    session_id: str
    subject: str
    tenant_id: str
    client_id: str | None = None
    authenticated_at: datetime | None = None
    expires_at: datetime | None = None
    ended_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class LogoutStateRecord:
    logout_id: str
    status: str
    session_id: str | None = None
    reason: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


class SessionServicePort(Protocol):
    async def create_session(
        self, request: SessionCreateRequest, /
    ) -> SessionRecord: ...

    async def get_session(
        self, session_id: str, /
    ) -> SessionRecord | None: ...

    async def terminate_session(
        self, session_id: str, /
    ) -> SessionRecord | None: ...

    async def logout_state(
        self, session_id: str, /
    ) -> LogoutStateRecord | None: ...


__all__ = [
    "LogoutStateRecord",
    "SessionCreateRequest",
    "SessionRecord",
    "SessionServicePort",
]
