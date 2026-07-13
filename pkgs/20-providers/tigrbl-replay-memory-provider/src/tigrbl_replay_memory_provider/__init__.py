"""Non-durable process-local replay reservation provider."""

from datetime import datetime, timezone
import secrets
import time
from threading import Lock, RLock

from tigrbl_identity_contracts.replay import ReplayReservationRequest, ReplayReservationResult
from tigrbl_identity_contracts.rp import LoginRequest, RPSession
from tigrbl_security_trust_contracts import DPoPNonceRecord
from tigrbl_replay_bases import ReplayReservationBase


class MemoryReplayProvider(ReplayReservationBase):
    provider_id = "replay:memory"
    persistence = "ephemeral-process-local"

    def __init__(self) -> None:
        self._reservations: dict[str, datetime] = {}
        self._lock = Lock()

    async def check_and_reserve(
        self, request: ReplayReservationRequest, /
    ) -> ReplayReservationResult:
        digest = self.digest_key(request.key)
        now = datetime.now(timezone.utc)
        with self._lock:
            expired = [key for key, expiry in self._reservations.items() if expiry <= now]
            for key in expired:
                self._reservations.pop(key, None)
            duplicate = digest in self._reservations
            if not duplicate:
                self._reservations[digest] = request.expires_at
        return ReplayReservationResult(
            not duplicate,
            digest,
            request.expires_at,
            duplicate=duplicate,
            provider_id=self.provider_id,
        )

    def contains_digest(self, digest: str) -> bool:
        with self._lock:
            return digest in self._reservations


class MemoryRPStateProvider:
    """Non-durable, process-local RP state provider for explicit injection."""

    provider_id = "rp-state:memory"
    persistence = "ephemeral-process-local"

    def __init__(self) -> None:
        self._items: dict[str, LoginRequest] = {}
        self._consumed: set[str] = set()
        self._lock = RLock()

    def create(self, *, redirect_uri: str, scope: tuple[str, ...]) -> LoginRequest:
        from tigrbl_security_proof_pkce import make_pkce_verifier

        request = LoginRequest(
            state=secrets.token_urlsafe(24), nonce=secrets.token_urlsafe(24),
            code_verifier=make_pkce_verifier(), redirect_uri=redirect_uri,
            scope=tuple(scope),
        )
        with self._lock:
            self._items[request.state] = request
        return request

    def consume(self, state: str) -> LoginRequest:
        with self._lock:
            if state in self._consumed:
                raise ValueError("callback state was already consumed")
            try:
                request = self._items.pop(state)
            except KeyError as exc:
                raise ValueError("unknown callback state") from exc
            self._consumed.add(state)
            return request


class MemoryRPSessionProvider:
    """Non-durable, process-local RP session provider for explicit injection."""

    provider_id = "rp-session:memory"
    persistence = "ephemeral-process-local"

    def __init__(self) -> None:
        self._sessions: dict[str, RPSession] = {}
        self._lock = RLock()

    def save(self, session_id: str, session: RPSession) -> None:
        with self._lock:
            self._sessions[session_id] = session

    def get(self, session_id: str) -> RPSession:
        with self._lock:
            try:
                return self._sessions[session_id]
            except KeyError as exc:
                raise ValueError("unknown RP session") from exc


class MemoryReplayCheckProvider:
    """Synchronous non-durable atomic replay provider."""

    provider_id = "replay-check:memory"
    persistence = "ephemeral-process-local"

    def __init__(self) -> None:
        self._entries: dict[str, int] = {}
        self._lock = RLock()

    def _purge(self, now: int) -> None:
        for key in [key for key, expiry in self._entries.items() if expiry <= now]:
            self._entries.pop(key, None)

    def check_and_store(self, key: str, *, now: int | None = None, ttl_s: int) -> bool:
        current = int(time.time()) if now is None else int(now)
        with self._lock:
            self._purge(current)
            duplicate = key in self._entries
            if not duplicate:
                self._entries[key] = current + max(int(ttl_s), 1)
            return duplicate

    def snapshot(self) -> dict[str, int]:
        with self._lock:
            self._purge(int(time.time()))
            return dict(self._entries)

    def clear(self) -> None:
        with self._lock:
            self._entries.clear()


class MemorySingleUseNonceProvider:
    """Synchronous non-durable single-use nonce provider."""

    provider_id = "single-use-nonce:memory"
    persistence = "ephemeral-process-local"

    def __init__(self) -> None:
        self._entries: dict[str, int] = {}
        self._lock = RLock()

    def _purge(self, now: int) -> None:
        for key in [key for key, expiry in self._entries.items() if expiry <= now]:
            self._entries.pop(key, None)

    def issue(self, *, ttl_s: int) -> str:
        return self.register(secrets.token_urlsafe(24), ttl_s=ttl_s)

    def register(self, nonce: str, *, ttl_s: int) -> str:
        with self._lock:
            now = int(time.time())
            self._purge(now)
            self._entries[str(nonce)] = now + max(int(ttl_s), 1)
        return str(nonce)

    def consume(self, nonce: str, *, now: int | None = None) -> bool:
        current = int(time.time()) if now is None else int(now)
        with self._lock:
            self._purge(current)
            expiry = self._entries.pop(str(nonce), None)
            return expiry is not None and expiry > current

    def snapshot(self) -> dict[str, DPoPNonceRecord]:
        with self._lock:
            self._purge(int(time.time()))
            return {key: DPoPNonceRecord(nonce=key, expires_at=expiry) for key, expiry in self._entries.items()}

    def clear(self) -> None:
        with self._lock:
            self._entries.clear()


__all__ = [
    "MemoryReplayCheckProvider", "MemoryReplayProvider", "MemoryRPSessionProvider",
    "MemoryRPStateProvider", "MemorySingleUseNonceProvider",
]
