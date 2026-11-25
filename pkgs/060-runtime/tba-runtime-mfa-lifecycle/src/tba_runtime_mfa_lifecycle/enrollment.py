"""Issue and complete MFA enrollment without exposing active credentials to the client."""

from __future__ import annotations

import secrets
from collections.abc import Callable, Mapping
from datetime import datetime, timedelta, timezone

from .contracts import (
    CeremonyKind,
    FactorAssurance,
    FactorAttempt,
    FactorBinding,
    FactorStore,
    FactorVerifier,
    LifecycleResult,
    LifecycleStatus,
)


class _FactorRuntime:
    def __init__(
        self,
        store: FactorStore,
        verifiers: Mapping[str, FactorVerifier],
        *,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        self._store = store
        self._verifiers = dict(verifiers)
        self._clock = clock or (lambda: datetime.now(timezone.utc))

    def _now(self) -> datetime:
        now = self._clock()
        if now.utcoffset() is None:
            raise ValueError("factor lifecycle timestamps must be timezone-aware")
        return now

    def _begin(
        self,
        binding: FactorBinding,
        kind: CeremonyKind,
        *,
        ttl: timedelta,
        credential_reference: str | None,
        replace_reference: str | None = None,
    ) -> LifecycleResult:
        if binding.factor not in self._verifiers or ttl <= timedelta(0):
            raise ValueError(
                "a registered factor verifier and positive TTL are required"
            )
        now = self._now()
        attempt = FactorAttempt(
            attempt_id=secrets.token_urlsafe(32),
            binding=binding,
            kind=kind,
            issued_at=now,
            expires_at=now + ttl,
            challenge=secrets.token_bytes(32),
            credential_reference=credential_reference,
            replace_reference=replace_reference,
        )
        self._store.create(attempt)
        return LifecycleResult(LifecycleStatus.CHALLENGE_REQUIRED, attempt=attempt)

    def _complete(
        self, attempt_id: str, binding: FactorBinding, proof: object, kind: CeremonyKind
    ) -> LifecycleResult:
        attempt = self._store.get(attempt_id)
        if attempt is None or attempt.binding != binding or attempt.kind != kind:
            return LifecycleResult(LifecycleStatus.REJECTED)
        now = self._now()
        if now >= attempt.expires_at:
            return LifecycleResult(LifecycleStatus.EXPIRED)
        verifier = self._verifiers.get(binding.factor)
        verified = verifier(attempt, proof, now) if verifier is not None else None
        if verified is None or not verified.method or not verified.replay_key:
            return LifecycleResult(LifecycleStatus.REJECTED)
        now = self._now()
        if now >= attempt.expires_at:
            return LifecycleResult(LifecycleStatus.EXPIRED)
        if not self._store.commit(attempt, verified, now=now):
            return LifecycleResult(LifecycleStatus.REJECTED)
        return LifecycleResult(
            LifecycleStatus.COMPLETED,
            assurance=FactorAssurance(binding, verified.method, now),
        )

    def _cancel(
        self, attempt_id: str, binding: FactorBinding, kind: CeremonyKind
    ) -> bool:
        attempt = self._store.get(attempt_id)
        return (
            attempt is not None
            and attempt.binding == binding
            and attempt.kind == kind
            and self._store.cancel(attempt)
        )


class EnrollmentRuntime(_FactorRuntime):
    def begin(
        self,
        binding: FactorBinding,
        *,
        credential_reference: str | None = None,
        replace_reference: str | None = None,
        ttl: timedelta = timedelta(minutes=5),
    ) -> LifecycleResult:
        return self._begin(
            binding,
            CeremonyKind.ENROLLMENT,
            ttl=ttl,
            credential_reference=credential_reference,
            replace_reference=replace_reference,
        )

    def complete(
        self, attempt_id: str, binding: FactorBinding, proof: object
    ) -> LifecycleResult:
        return self._complete(attempt_id, binding, proof, CeremonyKind.ENROLLMENT)

    def cancel(self, attempt_id: str, binding: FactorBinding) -> bool:
        return self._cancel(attempt_id, binding, CeremonyKind.ENROLLMENT)
