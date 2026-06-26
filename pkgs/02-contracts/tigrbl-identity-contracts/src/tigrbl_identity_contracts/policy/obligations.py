"""Policy obligation and advice contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Protocol

from .decisions import PolicyDecision


@dataclass(frozen=True, slots=True)
class Obligation:
    obligation_id: str
    attributes: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class Advice:
    advice_id: str
    attributes: Mapping[str, Any] = field(default_factory=dict)


class ObligationHandlerPort(Protocol):
    async def handle_obligation(self, obligation: Obligation, decision: PolicyDecision, /) -> None: ...


class AdviceHandlerPort(Protocol):
    async def handle_advice(self, advice: Advice, decision: PolicyDecision, /) -> None: ...


__all__ = ["Advice", "AdviceHandlerPort", "Obligation", "ObligationHandlerPort"]
