"""Deprecated Security Event replay-store compatibility surface."""

from datetime import datetime, timedelta, timezone
from warnings import warn

from tigrbl_identity_contracts.replay import ReplayKey, ReplayReservationRequest
from tigrbl_replay_memory_provider import MemoryReplayProvider
from tigrbl_security_event_bases import SecurityEventReplayBase

warn(
    "tigrbl-security-event-replay-store is deprecated; use "
    "tigrbl-replay-memory-provider or a durable replay repository",
    DeprecationWarning,
    stacklevel=2,
)


class InMemorySecurityEventReplayStore(SecurityEventReplayBase):
    """Legacy synchronous adapter; intentionally non-durable."""

    def __init__(self) -> None:
        self._provider = MemoryReplayProvider()
        self._consumed: set[tuple[str, str]] = set()

    def consume_once(self, issuer: str, token_id: str, /) -> bool:
        if not issuer or not token_id:
            raise ValueError("issuer and token ID are required")
        key = (issuer, token_id)
        if key in self._consumed:
            return False
        self._consumed.add(key)
        return True

    def contains(self, issuer: str, token_id: str) -> bool:
        return (issuer, token_id) in self._consumed


__all__ = ["InMemorySecurityEventReplayStore"]
