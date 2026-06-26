"""OAuth scope matching contracts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class ScopeMatchRequest:
    granted: tuple[str, ...]
    required: tuple[str, ...]
    mode: str = "all"


@dataclass(frozen=True, slots=True)
class ScopeMatchResult:
    allowed: bool
    granted: tuple[str, ...]
    required: tuple[str, ...]
    missing: tuple[str, ...] = ()


class ScopeMatcherPort(Protocol):
    def match(self, request: ScopeMatchRequest, /) -> ScopeMatchResult: ...


__all__ = ["ScopeMatchRequest", "ScopeMatchResult", "ScopeMatcherPort"]
