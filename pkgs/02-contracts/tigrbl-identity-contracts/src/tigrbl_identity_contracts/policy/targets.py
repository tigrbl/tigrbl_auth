"""Policy target contracts."""

from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module
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


_SCHEMA_EXPORTS = {
    "PolicyTargetCreateRequest",
    "PolicyTargetReadResponse",
    "PolicyTargetUpdateRequest",
}


def __getattr__(name: str) -> Any:
    if name not in _SCHEMA_EXPORTS:
        raise AttributeError(name)
    value = getattr(import_module("tigrbl_identity_contracts.schemas"), name)
    globals()[name] = value
    return value


__all__ = [
    "TargetMatchRequest",
    "TargetMatchResult",
    "TargetMatcherPort",
]
