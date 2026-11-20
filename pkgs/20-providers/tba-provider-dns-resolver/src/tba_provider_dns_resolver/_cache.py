"""TTL-aware cache for DNS resolver responses."""

from collections import OrderedDict
from dataclasses import dataclass, replace
from threading import RLock
from time import monotonic

from tba_codec_dns.rdata import decoded
from tba_codec_dns.wire import Message, RecordType

_CacheKey = tuple


@dataclass(frozen=True)
class CacheStatistics:
    hits: int
    misses: int


class Cache:
    """Bounded thread-safe TTL cache with least-recently-used eviction."""

    def __init__(self, size: int = 256):
        if size <= 0:
            raise ValueError("DNS cache size must be positive")
        self.size = size
        self._data: OrderedDict[_CacheKey, tuple[Message, float, float]] = OrderedDict()
        self._lock = RLock()
        self._hits = 0
        self._misses = 0

    def get(self, key: _CacheKey) -> Message | None:
        with self._lock:
            entry = self._data.get(key)
            if entry is None:
                self._misses += 1
                return None
            message, inserted, expires = entry
            now = monotonic()
            if now >= expires:
                del self._data[key]
                self._misses += 1
                return None
            self._hits += 1
            self._data.move_to_end(key)
            age = int(now - inserted)

            def age_records(records):
                return tuple(
                    rr
                    if rr.type in (RecordType.OPT, RecordType.TSIG)
                    else replace(rr, ttl=max(0, rr.ttl - age))
                    for rr in records
                )

            return replace(
                message,
                answers=age_records(message.answers),
                authority=age_records(message.authority),
                additional=age_records(message.additional),
            )

    def put(self, key: _CacheKey, message: Message) -> None:
        if message.rcode not in (0, 3) or any(
            rr.type == RecordType.TSIG for rr in message.additional
        ):
            return
        ttl = min(
            (
                rr.ttl
                for rr in (*message.answers, *message.authority)
                if rr.type != RecordType.OPT
            ),
            default=0,
        )
        if message.rcode == 3 or not message.answers:
            soa = next(
                (rr for rr in message.authority if rr.type == RecordType.SOA), None
            )
            if soa is None:
                return
            ttl = min(ttl, decoded(soa)[-1])
        if ttl <= 0:
            return
        with self._lock:
            now = monotonic()
            self._data[key] = (message, now, now + ttl)
            self._data.move_to_end(key)
            if len(self._data) > self.size:
                self._data.popitem(last=False)

    def clear(self) -> None:
        with self._lock:
            self._data.clear()

    def flush(self, key: _CacheKey | None = None) -> None:
        with self._lock:
            if key is None:
                self._data.clear()
            else:
                self._data.pop(key, None)

    def get_statistics_snapshot(self) -> CacheStatistics:
        with self._lock:
            return CacheStatistics(self._hits, self._misses)

    def reset_statistics(self) -> None:
        with self._lock:
            self._hits = self._misses = 0
