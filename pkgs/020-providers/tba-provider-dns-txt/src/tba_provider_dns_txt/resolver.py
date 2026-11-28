import math
from collections.abc import Iterable
from typing import Protocol

from tba_codec_dns.wire import WireError
from tba_provider_dns_resolver.client import NXDOMAIN, NoAnswer, Resolver

from .contracts import TxtResult, TxtStatus


class _TxtRecord(Protocol):
    @property
    def strings(self) -> tuple[bytes, ...]: ...


class _Resolver(Protocol):
    def resolve(
        self, name: str, rdtype: str, *, search: bool, lifetime: float
    ) -> Iterable[_TxtRecord]: ...


class DnsTxtResolver:
    def __init__(
        self, *, timeout: float = 3, resolver: _Resolver | None = None
    ) -> None:
        if not math.isfinite(timeout) or timeout <= 0:
            raise ValueError("DNS timeout must be finite and positive")
        self._timeout = timeout
        self._resolver = resolver if resolver is not None else Resolver(timeout=timeout)

    def lookup_txt(self, name: str, /) -> TxtResult:
        try:
            answer = self._resolver.resolve(
                name.removesuffix(".") + ".",
                "TXT",
                search=False,
                lifetime=self._timeout,
            )
            records = tuple(b"".join(record.strings) for record in answer)
        except (NXDOMAIN, NoAnswer):
            return TxtResult(TxtStatus.ABSENT)
        except (OSError, WireError):
            return TxtResult(TxtStatus.TEMPORARY_FAILURE)
        return TxtResult(TxtStatus.FOUND, records)
