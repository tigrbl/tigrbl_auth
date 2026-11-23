from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class AdaptiveContext:
    tenant_id: str
    trusted_network: bool
    trusted_device: bool
    ip_country: str
    local_hour: int
    known_countries: tuple[str, ...] = ()
    anomaly_detected: bool = False


@dataclass(frozen=True, slots=True)
class AdaptiveDecision:
    allowed: bool
    step_up_required: bool
    risk_level: str
    reasons: tuple[str, ...]
    amr: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class RelationshipDefinition:
    resource_type: str
    relation: str
    subject_types: tuple[str, ...]
    version: int


@dataclass(frozen=True, slots=True)
class RelationshipTuple:
    resource: str
    relation: str
    subject: str
    tenant_id: str


@dataclass(frozen=True, slots=True)
class GraphDecision:
    allowed: bool
    reason: str
    explanation: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class AccessDecisionRequest:
    tenant_id: str
    subject: str
    action: str
    resource: str
    context: Mapping[str, Any]
    correlation_id: str
    policy_version_id: str | None = None


@dataclass(frozen=True, slots=True)
class AccessDecisionResponse:
    allowed: bool
    reason: str
    correlation_id: str
    policy_version_id: str
    explanation: tuple[str, ...]
    idempotency_key: str


@dataclass(frozen=True, slots=True)
class AuthTelemetryEvent:
    event_id: str
    tenant_id: str
    subject_id: str
    event_type: str
    correlation_id: str
    ip_country: str
    trusted_device: bool
    outcome: str
    details: Mapping[str, Any]
    recorded_at: str


@dataclass(frozen=True, slots=True)
class AnomalySignal:
    signal_id: str
    tenant_id: str
    subject_id: str
    correlation_id: str
    severity: str
    reasons: tuple[str, ...]
    recommended_action: str
    redacted_details: Mapping[str, Any]


@dataclass(frozen=True, slots=True)
class AdaptiveTrustDomain:
    name: str
    issuers: tuple[str, ...]
    clouds: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class TrustEdge:
    source_domain: str
    target_domain: str
    exchange_kind: str
    constraints: Mapping[str, Any]
    revoked: bool = False


@dataclass(frozen=True, slots=True)
class TrustPath:
    source_domain: str
    target_domain: str
    hops: tuple[str, ...]
    exchange_kinds: tuple[str, ...]


__all__ = [
    "AccessDecisionRequest",
    "AccessDecisionResponse",
    "AdaptiveContext",
    "AdaptiveDecision",
    "AnomalySignal",
    "AuthTelemetryEvent",
    "GraphDecision",
    "RelationshipDefinition",
    "RelationshipTuple",
    "AdaptiveTrustDomain",
    "TrustEdge",
    "TrustPath",
]

# Compatibility alias. New code should use the unambiguous family name.
TrustDomain = AdaptiveTrustDomain
