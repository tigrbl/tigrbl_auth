from __future__ import annotations

import threading
from datetime import datetime, timezone


class _BackchannelReplayStore:
    def __init__(self) -> None:
        self._items: dict[str, datetime] = {}
        self._lock = threading.Lock()

    def _cleanup(self, now: datetime) -> None:
        for key in [item for item, expiry in self._items.items() if expiry <= now]:
            self._items.pop(key, None)

    def register(self, jti: str, *, exp: datetime, now: datetime) -> None:
        with self._lock:
            self._cleanup(now)
            if jti in self._items and self._items[jti] > now:
                raise ValueError("replayed logout token")
            self._items[jti] = exp

    def snapshot(self) -> dict[str, int]:
        now = datetime.now(timezone.utc)
        with self._lock:
            self._cleanup(now)
            return {"active_logout_jti": len(self._items)}


__all__ = ["_BackchannelReplayStore"]
