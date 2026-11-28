from __future__ import annotations

from collections.abc import Callable
from secrets import token_urlsafe
from time import time
from urllib.parse import urlencode

from .contracts import (
    LogoutAttempt,
    LogoutAttempts,
    LogoutRejected,
    LogoutRequest,
    LogoutResult,
    LogoutRevoker,
    LogoutSession,
    LogoutStatus,
    LogoutValidator,
    ValidatedLogout,
)


def append_logout_state(redirect_uri: str | None, state: str | None) -> str | None:
    if redirect_uri is None or not state:
        return redirect_uri
    base, marker, fragment = redirect_uri.partition("#")
    separator = "&" if "?" in base else "?"
    return base + separator + urlencode({"state": state}) + marker + fragment


class LogoutRuntime:
    """Coordinate validated requests and atomically consumed browser attempts."""

    def __init__(
        self,
        validate: LogoutValidator,
        revoke: LogoutRevoker,
        attempts: LogoutAttempts,
        *,
        ttl_seconds: float = 300,
        now: Callable[[], float] = time,
    ) -> None:
        if not 0 < ttl_seconds <= 900:
            raise ValueError("logout attempt TTL must be between zero and 900 seconds")
        self.validate = validate
        self.revoke = revoke
        self.attempts = attempts
        self.ttl_seconds = ttl_seconds
        self.now = now

    async def _save(
        self,
        request: LogoutRequest,
        session: LogoutSession | None,
        client_id: str | None,
        browser_binding: str,
        *,
        confirmation: bool,
    ) -> LogoutResult:
        if not request.issuer or not browser_binding:
            return LogoutResult(LogoutStatus.REJECTED)
        token = token_urlsafe(32)
        attempt = LogoutAttempt(
            request,
            session,
            client_id,
            browser_binding,
            self.now() + self.ttl_seconds,
            confirmation,
        )
        try:
            await self.attempts.save(token, attempt)
        except OSError:
            return LogoutResult(LogoutStatus.UNAVAILABLE)
        status = (
            LogoutStatus.CONFIRMATION_REQUIRED
            if confirmation
            else LogoutStatus.HANDOFF_REQUIRED
        )
        return LogoutResult(status, token=token)

    async def handoff(
        self, request: LogoutRequest, *, browser_binding: str
    ) -> LogoutResult:
        """Stage a cross-site request without treating it as an authenticated session."""
        return await self._save(
            request, None, None, browser_binding, confirmation=False
        )

    async def _validated(
        self, request: LogoutRequest, session: LogoutSession | None
    ) -> ValidatedLogout:
        if not request.issuer or (
            session is not None and session.issuer != request.issuer
        ):
            raise LogoutRejected("logout issuer does not match the browser session")
        validated = await self.validate(request, session)
        if validated.redirect_uri != request.post_logout_redirect_uri:
            raise LogoutRejected(
                "logout validation did not confirm the exact redirect URI"
            )
        if request.client_id is not None and validated.client_id != request.client_id:
            raise LogoutRejected(
                "logout validation did not confirm the requested client"
            )
        if validated.redirect_uri is not None and validated.client_id is None:
            raise LogoutRejected("logout redirect has no verified client")
        return validated

    async def _complete(
        self,
        request: LogoutRequest,
        session: LogoutSession,
        validated: ValidatedLogout,
    ) -> LogoutResult:
        redirect = append_logout_state(validated.redirect_uri, request.state)
        if not await self.revoke(session, validated):
            return LogoutResult(LogoutStatus.UNAVAILABLE)
        return LogoutResult(LogoutStatus.COMPLETED, redirect, session=session)

    async def begin(
        self,
        request: LogoutRequest,
        session: LogoutSession | None,
        *,
        browser_binding: str,
    ) -> LogoutResult:
        try:
            validated = await self._validated(request, session)
            if session is None:
                return LogoutResult(
                    LogoutStatus.NO_SESSION,
                    append_logout_state(validated.redirect_uri, request.state),
                )
            if request.id_token_hint and validated.hint_matches_session:
                return await self._complete(request, session, validated)
            return await self._save(
                request,
                session,
                validated.client_id,
                browser_binding,
                confirmation=True,
            )
        except LogoutRejected:
            return LogoutResult(LogoutStatus.REJECTED)
        except OSError:
            return LogoutResult(LogoutStatus.UNAVAILABLE)

    async def resume(
        self,
        token: str,
        issuer: str,
        session: LogoutSession | None,
        *,
        browser_binding: str,
        confirmed: bool | None = None,
    ) -> LogoutResult:
        if not token or not issuer or not browser_binding:
            return LogoutResult(LogoutStatus.REJECTED)
        try:
            now = self.now()
            attempt = await self.attempts.consume(
                token, issuer=issuer, browser_binding=browser_binding, now=now
            )
            if (
                attempt is None
                or attempt.request.issuer != issuer
                or attempt.browser_binding != browser_binding
                or attempt.expires_at <= now
                or attempt.confirmation != (confirmed is not None)
            ):
                return LogoutResult(LogoutStatus.REJECTED)
            if not attempt.confirmation:
                return await self.begin(
                    attempt.request, session, browser_binding=browser_binding
                )
            if session is None or session != attempt.session:
                return LogoutResult(LogoutStatus.REJECTED)
            if confirmed is False:
                return LogoutResult(LogoutStatus.CANCELLED)
            validated = await self._validated(attempt.request, session)
            if validated.client_id != attempt.client_id:
                return LogoutResult(LogoutStatus.REJECTED)
            return await self._complete(attempt.request, session, validated)
        except LogoutRejected:
            return LogoutResult(LogoutStatus.REJECTED)
        except OSError:
            return LogoutResult(LogoutStatus.UNAVAILABLE)
