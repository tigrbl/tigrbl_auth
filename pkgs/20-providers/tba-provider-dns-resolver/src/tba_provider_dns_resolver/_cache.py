"""TTL-aware cache for DNS resolver responses."""

from collections import OrderedDict
from dataclasses import dataclass, replace
from threading import RLock
from time import monotonic, time

from tba_codec_dns.rdata import decoded
from tba_codec_dns.wire import Message, RecordType

_CacheKey = tuple


@dataclass(frozen=True)
class CacheStatistics:
    hits: int = 0
    misses: int = 0


class Cache:
    """Thread-safe DNS cache with periodic expiration cleanup."""

    def __init__(self, cleaning_interval: float = 300.0, *, size: int | None = None):
        if cleaning_interval <= 0 or (size is not None and size <= 0):
            raise ValueError("DNS cache limits must be positive")
        self.cleaning_interval = cleaning_interval
        self.next_cleaning = monotonic() + cleaning_interval
        self.size = size
        self._data: OrderedDict[_CacheKey, tuple[object, float, float]] = OrderedDict()
        self._key_hits: dict[_CacheKey, int] = {}
        self._lock = RLock()
        self._hits = 0
        self._misses = 0

    def _remove(self, key):
        self._data.pop(key, None)
        self._key_hits.pop(key, None)

    def _clean(self, now):
        if now >= self.next_cleaning:
            for key in tuple(self._data):
                if self._data[key][2] <= now:
                    self._remove(key)
            self.next_cleaning = now + self.cleaning_interval

    def get(self, key: _CacheKey):
        return self._get(key, age_answer=False)

    def _get(self, key, *, age_answer):
        with self._lock:
            now = monotonic()
            self._clean(now)
            entry = self._data.get(key)
            if entry is None:
                self._misses += 1
                return None
            message, inserted, expires = entry
            if now >= expires:
                self._remove(key)
                self._misses += 1
                return None
            self._hits += 1
            self._key_hits[key] += 1
            self._data.move_to_end(key)
            age = int(now - inserted)
            if not isinstance(message, Message):
                if not age_answer or not age or message.rrset is None:
                    return message
                rrset = message.rrset
                return replace(
                    message,
                    rrset=replace(
                        rrset,
                        ttl=max(0, rrset.ttl - age),
                        records=tuple(
                            replace(rr, ttl=max(0, rr.ttl - age))
                            for rr in rrset.records
                        ),
                    ),
                )

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

    def put(self, key: _CacheKey, message) -> None:
        if not isinstance(message, Message):
            self._put(key, message, message.expiration - time())
            return
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
        self._put(key, message, ttl)

    def _put(self, key, value, ttl):
        with self._lock:
            now = monotonic()
            self._clean(now)
            self._remove(key)
            if ttl > 0:
                self._data[key] = (value, now, now + ttl)
                self._key_hits[key] = 0
            if self.size is not None and len(self._data) > self.size:
                self._remove(next(iter(self._data)))

    def clear(self) -> None:
        self.flush()

    def flush(self, key: _CacheKey | None = None) -> None:
        with self._lock:
            if key is None:
                self._data.clear()
                self._key_hits.clear()
            else:
                self._remove(key)

    def get_statistics_snapshot(self) -> CacheStatistics:
        with self._lock:
            return CacheStatistics(self._hits, self._misses)

    def reset_statistics(self) -> None:
        with self._lock:
            self._hits = self._misses = 0


class LRUCache(Cache):
    """Bounded DNS answer cache tracking hits per entry."""

    def __init__(self, max_size: int = 100000):
        super().__init__(size=max_size)

    @property
    def max_size(self):
        return self.size

    def get_hits_for_key(self, key):
        with self._lock:
            entry = self._data.get(key)
            if entry is None or entry[2] <= monotonic():
                return 0
            return self._key_hits[key]
