"""Lifecycle for a provider's pending authorization request."""

from collections.abc import Callable
from datetime import datetime, timedelta
from secrets import token_urlsafe
from typing import Generic, TypeVar

from .contracts import (
    ContinuationOutcome,
    ContinuationRepository,
    PendingContinuation,
    Restart,
    Resume,
    StayLocal,
    ValidatedAuthorizationRequest,
)


Assurance = TypeVar("Assurance")


class HostedSignInContinuationRuntime(Generic[Assurance]):
    """Suspend and resolve already validated authorization requests."""

    def __init__(
        self,
        repository: ContinuationRepository,
        *,
        clock: Callable[[], datetime],
        client_is_active: Callable[[ValidatedAuthorizationRequest], bool],
        browser_matches: Callable[[str, str], bool],
        assurance_is_sufficient: Callable[[PendingContinuation, Assurance], bool],
        lifetime: timedelta,
        recovery_window: timedelta = timedelta(),
    ) -> None:
        if lifetime <= timedelta() or recovery_window < timedelta():
            raise ValueError("Continuation lifetime and recovery window are invalid")
        self._repository = repository
        self._clock = clock
        self._client_is_active = client_is_active
        self._browser_matches = browser_matches
        self._assurance_is_sufficient = assurance_is_sufficient
        self._lifetime = lifetime
        self._recovery_window = recovery_window

    def begin(
        self,
        request: ValidatedAuthorizationRequest,
        *,
        browser_binding: str,
        required_assurance: str | None = None,
    ) -> str:
        """Store an already validated request and return its opaque flow ID."""
        if not browser_binding:
            raise ValueError("Browser binding is required")
        now = self._clock()
        expires_at = now + self._lifetime
        pending = PendingContinuation(
            flow_id=token_urlsafe(32),
            request=request,
            browser_binding=browser_binding,
            started_at=now,
            expires_at=expires_at,
            recover_until=expires_at + self._recovery_window,
            required_assurance=required_assurance,
        )
        self._repository.insert(pending)
        return pending.flow_id

    def resolve(
        self,
        flow_id: str,
        *,
        issuer: str,
        tenant_id: str,
        browser_binding: str,
        assurance: Assurance,
    ) -> ContinuationOutcome:
        """Expose the request only after successful one-time consumption."""
        pending = self._repository.get_pending(flow_id)
        if pending is None or not browser_binding:
            return StayLocal()
        request = pending.request
        if (
            request.issuer != issuer
            or request.tenant_id != tenant_id
            or not self._browser_matches(pending.browser_binding, browser_binding)
            or not self._client_is_active(request)
        ):
            return StayLocal()
        now = self._clock()
        if now >= pending.expires_at:
            return Restart(request.client_id) if now < pending.recover_until else StayLocal()
        if not self._assurance_is_sufficient(pending, assurance):
            return StayLocal()
        now = self._clock()
        if now >= pending.expires_at:
            return Restart(request.client_id) if now < pending.recover_until else StayLocal()
        if not self._repository.consume_pending(pending, now=now):
            return StayLocal()
        return Resume(request)
