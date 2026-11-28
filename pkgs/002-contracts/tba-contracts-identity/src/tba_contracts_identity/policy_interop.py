"""AuthZEN wire and XACML adapter-neutral policy contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence


@dataclass(frozen=True, slots=True)
class AccessEvaluationRequest:
    subject: Mapping[str, Any]
    action: Mapping[str, Any]
    resource: Mapping[str, Any]
    context: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class AccessEvaluationResponse:
    decision: bool
    context: Mapping[str, Any] = field(default_factory=dict)
    obligations: Sequence[Mapping[str, Any]] = ()


@dataclass(frozen=True, slots=True)
class XacmlDecision:
    """Deprecated wire-shaped compatibility result.

    New code should use ``policy.xacml_mapping.XacmlDecisionResult`` and keep
    AuthZEN/XACML conversion in layer 50.
    """

    decision: str
    status: Mapping[str, Any] = field(default_factory=dict)
    obligations: Sequence[Mapping[str, Any]] = ()
    advice: Sequence[Mapping[str, Any]] = ()


def xacml_to_authzen(value: XacmlDecision) -> AccessEvaluationResponse:
    if value.decision not in {"Permit", "Deny", "NotApplicable", "Indeterminate"}:
        raise ValueError("unknown XACML decision")
    return AccessEvaluationResponse(value.decision == "Permit", {"xacml_status": dict(value.status)}, value.obligations)


__all__ = ["AccessEvaluationRequest", "AccessEvaluationResponse", "XacmlDecision", "xacml_to_authzen"]
