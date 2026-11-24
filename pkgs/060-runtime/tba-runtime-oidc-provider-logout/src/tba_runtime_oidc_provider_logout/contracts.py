from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from enum import Enum
from typing import Protocol


@dataclass(frozen=True)
class LogoutRequest:
    issuer: str
    client_id: str | None = None
    id_token_hint: str | None = None
    post_logout_redirect_uri: str | None = None
    state: str | None = None


@dataclass(frozen=True)
class LogoutSession:
    issuer: str
    session_id: str
    subject: str


@dataclass(frozen=True)
class ValidatedLogout:
    client_id: str | None
    redirect_uri: str | None
    hint_matches_session: bool = False


class LogoutRejected(ValueError):
    """The request or its session binding could not be authenticated."""


class LogoutStatus(str, Enum):
    HANDOFF_REQUIRED = "handoff_required"
    CONFIRMATION_REQUIRED = "confirmation_required"
    COMPLETED = "completed"
    NO_SESSION = "no_session"
    CANCELLED = "cancelled"
    REJECTED = "rejected"
    UNAVAILABLE = "unavailable"


@dataclass(frozen=True)
class LogoutResult:
    status: LogoutStatus
    redirect_uri: str | None = None
    token: str | None = None
    session: LogoutSession | None = None


@dataclass(frozen=True)
class LogoutAttempt:
    request: LogoutRequest
    session: LogoutSession | None
    client_id: str | None
    browser_binding: str
    expires_at: float
    confirmation: bool


class LogoutAttempts(Protocol):
    async def save(self, token: str, attempt: LogoutAttempt) -> None: ...

    async def consume(
        self, token: str, *, issuer: str, browser_binding: str, now: float
    ) -> LogoutAttempt | None:
        """Atomically return and remove a matching, unexpired attempt."""
        ...


LogoutValidator = Callable[
    [LogoutRequest, LogoutSession | None], Awaitable[ValidatedLogout]
]
LogoutRevoker = Callable[[LogoutSession, ValidatedLogout], Awaitable[bool]]
