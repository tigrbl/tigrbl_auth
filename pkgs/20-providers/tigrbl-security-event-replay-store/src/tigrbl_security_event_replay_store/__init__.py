from threading import Lock

from tigrbl_security_event_bases import SecurityEventReplayBase


class InMemorySecurityEventReplayStore(SecurityEventReplayBase):
    def __init__(self):
        self._consumed: set[tuple[str, str]] = set()
        self._lock = Lock()

    def consume_once(self, issuer: str, token_id: str, /) -> bool:
        if not issuer or not token_id:
            raise ValueError("issuer and token ID are required")
        key = (issuer, token_id)
        with self._lock:
            if key in self._consumed:
                return False
            self._consumed.add(key)
            return True

    def contains(self, issuer: str, token_id: str) -> bool:
        with self._lock:
            return (issuer, token_id) in self._consumed


__all__ = ["InMemorySecurityEventReplayStore"]
