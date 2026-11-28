"""Browser-bound hosted OIDC/OAuth authorization continuation."""

from __future__ import annotations

import hashlib
import secrets
from collections.abc import Callable
from datetime import datetime, timedelta, timezone

from .contracts import (
    AuthenticationEvidence,
    ContinuationReason,
    ContinuationRecord,
    ContinuationRequirements,
    ContinuationResult,
    ContinuationStatus,
    ContinuationStore,
    ContinuationUnavailable,
    ValidatedAuthorizationRequest,
    require_aware,
)


def _browser_digest(value: str) -> bytes:
    return hashlib.sha256(value.encode("utf-8")).digest()


class HostedAuthorizationContinuation:
    def __init__(
        self,
        store: ContinuationStore,
        *,
        clock: Callable[[], datetime] | None = None,
        recovery_window: timedelta = timedelta(),
    ) -> None:
        if recovery_window < timedelta():
            raise ValueError("recovery window must be nonnegative")
        self._recovery_window = recovery_window
        self._store = store
        self._clock = clock or (lambda: datetime.now(timezone.utc))

    def _now(self) -> datetime:
        now = self._clock()
        require_aware(now)
        return now

    def begin(
        self,
        request: ValidatedAuthorizationRequest,
        *,
        browser_transaction_id: str,
        requirements: ContinuationRequirements = ContinuationRequirements(),
        ttl: timedelta = timedelta(minutes=30),
    ) -> ContinuationRecord:
        if not browser_transaction_id or ttl <= timedelta(0):
            raise ValueError("a browser transaction ID and positive TTL are required")
        now = self._now()
        record = ContinuationRecord(
            flow_id=secrets.token_urlsafe(32),
            browser_digest=_browser_digest(browser_transaction_id),
            request=request,
            requirements=requirements,
            issued_at=now,
            expires_at=now + ttl,
        )
        self._store.create(record)
        return record

    def _lookup(
        self,
        flow_id: str,
        *,
        issuer: str,
        browser_transaction_id: str,
        client_id: str,
        tenant_id: str | None,
    ) -> ContinuationRecord | None:
        if not flow_id or not browser_transaction_id:
            return None
        record = self._store.get(flow_id)
        if (
            record is None
            or record.flow_id != flow_id
            or record.request.issuer != issuer
            or record.request.client_id != client_id
            or getattr(record.request, "tenant_id", None) != tenant_id
            or not secrets.compare_digest(
                record.browser_digest, _browser_digest(browser_transaction_id)
            )
        ):
            return None
        return record

    def inspect(
        self,
        flow_id: str,
        *,
        issuer: str,
        browser_transaction_id: str,
        client_id: str,
        tenant_id: str | None = None,
    ) -> ContinuationRecord | None:
        """Read a pending flow for policy/UI decisions without consuming it."""
        record = self._lookup(
            flow_id,
            issuer=issuer,
            browser_transaction_id=browser_transaction_id,
            client_id=client_id,
            tenant_id=tenant_id,
        )
        if record is None or self._now() >= record.expires_at:
            return None
        return record

    def _expired_result(
        self, record: ContinuationRecord, now: datetime
    ) -> ContinuationResult:
        return ContinuationResult(
            ContinuationStatus.RESTART_REQUIRED,
            reason=ContinuationReason.INVALID_FLOW,
            restart_client_id=(
                record.request.client_id
                if now - record.expires_at < self._recovery_window
                else None
            ),
        )

    def resume(
        self,
        flow_id: str,
        *,
        issuer: str,
        browser_transaction_id: str,
        client_id: str,
        evidence: AuthenticationEvidence | None,
        registration_is_current: Callable[[ValidatedAuthorizationRequest], bool],
        tenant_id: str | None = None,
    ) -> ContinuationResult:
        try:
            record = self._lookup(
                flow_id,
                issuer=issuer,
                browser_transaction_id=browser_transaction_id,
                client_id=client_id,
                tenant_id=tenant_id,
            )
            if record is None:
                return ContinuationResult(
                    ContinuationStatus.RESTART_REQUIRED,
                    reason=ContinuationReason.INVALID_FLOW,
                )
            now = self._now()
            if now - record.expires_at >= self._recovery_window:
                return self._expired_result(record, now)
            if not registration_is_current(record.request):
                return ContinuationResult(
                    ContinuationStatus.RESTART_REQUIRED,
                    reason=ContinuationReason.REGISTRATION_CHANGED,
                )
            requirements = record.requirements
            now = self._now()
            if now >= record.expires_at:
                return self._expired_result(record, now)
            if (
                evidence is None
                or not evidence.subject
                or evidence.authenticated_at > now
                or (
                    requirements.subject is not None
                    and requirements.subject != evidence.subject
                )
                or (
                    requirements.not_before is not None
                    and evidence.authenticated_at < requirements.not_before
                )
                or not requirements.required_methods.issubset(evidence.methods)
            ):
                return ContinuationResult(
                    ContinuationStatus.UNAVAILABLE,
                    reason=ContinuationReason.AUTHENTICATION_REQUIRED,
                )
            now = self._now()
            if now >= record.expires_at:
                return self._expired_result(record, now)
            if not self._store.consume(record, now=now):
                return ContinuationResult(
                    ContinuationStatus.RESTART_REQUIRED,
                    reason=ContinuationReason.INVALID_FLOW,
                )
        except ContinuationUnavailable:
            return ContinuationResult(
                ContinuationStatus.UNAVAILABLE,
                reason=ContinuationReason.STORAGE_UNAVAILABLE,
            )
        return ContinuationResult(ContinuationStatus.RESUME, request=record.request)
