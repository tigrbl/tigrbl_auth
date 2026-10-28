"""Authentication context contracts for ACR and AMR evaluation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class AcrValue:
    value: str

    def __post_init__(self) -> None:
        cleaned = self.value.strip()
        if not cleaned:
            raise ValueError("ACR value is required")
        object.__setattr__(self, "value", cleaned)


@dataclass(frozen=True, slots=True)
class AmrValue:
    value: str

    def __post_init__(self) -> None:
        cleaned = self.value.strip()
        if not cleaned:
            raise ValueError("AMR value is required")
        object.__setattr__(self, "value", cleaned)


@dataclass(frozen=True, slots=True)
class AcrEvaluationRequest:
    requested: tuple[AcrValue | str, ...] = ()
    achieved: AcrValue | str | None = None
    context: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class AcrEvaluationResult:
    satisfied: bool
    acr: AcrValue | str | None = None
    reason: str | None = None


@dataclass(frozen=True, slots=True)
class AmrEvaluationRequest:
    required: tuple[AmrValue | str, ...] = ()
    achieved: tuple[AmrValue | str, ...] = ()
    context: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class AmrEvaluationResult:
    satisfied: bool
    achieved: tuple[AmrValue | str, ...] = ()
    missing: tuple[AmrValue | str, ...] = ()
    reason: str | None = None


__all__ = [
    "AcrEvaluationRequest",
    "AcrEvaluationResult",
    "AcrValue",
    "AmrEvaluationRequest",
    "AmrEvaluationResult",
    "AmrValue",
]
