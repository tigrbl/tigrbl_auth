"""Policy target contracts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Protocol

from .requests import PolicyRequest


@dataclass(frozen=True, slots=True)
class TargetMatchRequest:
    request: PolicyRequest
    target: Mapping[str, Any]


@dataclass(frozen=True, slots=True)
class TargetMatchResult:
    matched: bool
    reason: str = ""
    matched_fields: tuple[str, ...] = ()


class TargetMatcherPort(Protocol):
    def matches_target(self, request: TargetMatchRequest, /) -> TargetMatchResult: ...


__all__ = [
    "TargetMatchRequest",
    "TargetMatchResult",
    "TargetMatcherPort",
]
