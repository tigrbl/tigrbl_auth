"""Non-durable process-local replay reservation provider."""

from datetime import datetime, timezone
from threading import Lock

from tigrbl_identity_contracts.replay import ReplayReservationRequest, ReplayReservationResult
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


__all__ = ["MemoryReplayProvider"]
