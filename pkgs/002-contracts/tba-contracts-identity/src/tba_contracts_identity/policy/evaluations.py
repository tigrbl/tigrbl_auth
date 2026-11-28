from dataclasses import dataclass, field
from typing import Mapping, Protocol

from .decisions import PolicyDecision
from .entities import PolicyEntityChain


@dataclass(frozen=True, slots=True)
class PolicyEvaluationRequest:
    subject: PolicyEntityChain
    action: PolicyEntityChain
    resource: PolicyEntityChain
    context: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class PolicyEvaluationResult:
    decision: PolicyDecision
    obligations: tuple[object, ...] = ()
    advice: tuple[object, ...] = ()


class PolicyEvaluationPort(Protocol):
    def evaluate(
        self, request: PolicyEvaluationRequest, /
    ) -> PolicyEvaluationResult: ...


__all__ = ["PolicyEvaluationPort", "PolicyEvaluationRequest", "PolicyEvaluationResult"]
