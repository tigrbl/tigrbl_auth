"""OIDC session service contracts backed by storage schemas."""

from __future__ import annotations

from typing import Protocol

from ..schemas import AuthSessionCreateRequest, AuthSessionReadResponse, LogoutStateReadResponse


class SessionServicePort(Protocol):
    async def create_session(self, request: AuthSessionCreateRequest, /) -> AuthSessionReadResponse: ...

    async def get_session(self, session_id: str, /) -> AuthSessionReadResponse | None: ...

    async def terminate_session(self, session_id: str, /) -> AuthSessionReadResponse | None: ...

    async def logout_state(self, session_id: str, /) -> LogoutStateReadResponse | None: ...


__all__ = [
    "AuthSessionCreateRequest",
    "AuthSessionReadResponse",
    "LogoutStateReadResponse",
    "SessionServicePort",
]
