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
class PasswordlessCredential:
    credential_id: str
    subject_id: str
    tenant_id: str
    credential_kind: str
    recovery_codes: tuple[str, ...]
    created_at: str
    revoked: bool = False


@dataclass(frozen=True, slots=True)
class MfaFactor:
    factor_id: str
    subject_id: str
    tenant_id: str
    method: str
    created_at: str
    bound_credential_id: str | None = None
    revoked: bool = False


@dataclass(frozen=True, slots=True)
class WebAuthnCredential:
    credential_id: str
    subject_id: str
    tenant_id: str
    rp_id: str
    algorithm: str
    transports: tuple[str, ...]
    created_at: str
    sign_count: int = 0
    revoked: bool = False


@dataclass(frozen=True, slots=True)
class AuthenticationChallenge:
    challenge_id: str
    subject_id: str
    tenant_id: str
    challenge_kind: str
    expected_nonce: str
    issued_at: str
    expires_at: str
    allowed_methods: tuple[str, ...]
    step_up_required: bool
    bound_credential_id: str | None = None
    consumed: bool = False


@dataclass(frozen=True, slots=True)
class IdentityProvider:
    provider_id: str
    tenant_id: str
    kind: str
    issuer: str
    discovery_url: str
    audience: str
    logout_supported: bool
    display_name: str
    claim_mapping: Mapping[str, str]
    scopes: tuple[str, ...]
    key_set_version: int = 1
    enabled: bool = True


@dataclass(frozen=True, slots=True)
class FederatedSession:
    session_id: str
    provider_id: str
    tenant_id: str
    issuer: str
    audience: str
    logout_supported: bool
    normalized_claims: Mapping[str, Any]
    bound_at: str


@dataclass(frozen=True, slots=True)
class DeviceIdentity:
    device_id: str
    subject_id: str
    tenant_id: str
    credential_posture: str
    last_ip_country: str | None
    created_at: str
    revoked: bool = False


@dataclass(frozen=True, slots=True)
class WorkloadIdentity:
    workload_id: str
    tenant_id: str
    trust_domain: str
    cloud: str
    namespace: str
    attestor: str
    credential_id: str
    created_at: str
    revoked: bool = False


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
class PolicyDefinition:
    policy_id: str
    name: str
    tenant_id: str
    language: str
    created_at: str


@dataclass(frozen=True, slots=True)
class PolicyVersion:
    version_id: str
    policy_id: str
    version_number: int
    source: str
    created_at: str
    relation: str
    context_equals: tuple[tuple[str, Any], ...]
    promoted: bool = False


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
class TrustDomain:
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


@dataclass(frozen=True, slots=True)
class AdvancedIdentityBoundaryFeature:
    feature_id: str
    category: str
    runtime_objects: tuple[str, ...]
    guarded_capabilities: tuple[str, ...]
