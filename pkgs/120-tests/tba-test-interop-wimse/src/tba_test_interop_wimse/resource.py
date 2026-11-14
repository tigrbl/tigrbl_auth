"""Observable state for a protected test resource."""

from threading import Lock


class WriteLedger:
    def __init__(self):
        self._writes = []
        self._lock = Lock()

    def commit(self, identity):
        with self._lock:
            self._writes.append(identity)

    def snapshot(self):
        with self._lock:
            return tuple(self._writes)
