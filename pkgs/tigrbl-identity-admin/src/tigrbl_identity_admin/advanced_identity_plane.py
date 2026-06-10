from __future__ import annotations

from collections import deque
from dataclasses import dataclass, replace
from datetime import datetime, timedelta, timezone
from typing import Any, Iterable, Mapping
from uuid import uuid4

from tigrbl_auth.rfc.rfc8176 import validate_amr_claim
from tigrbl_auth.rfc.rfc8812 import is_webauthn_algorithm

SECRET_FIELD_TOKENS: tuple[str, ...] = (
    "secret",
    "password",
    "token",
    "assertion",
    "private_key",
    "client_secret",
)


def _utc_now() -> datetime:
    return datetime.now(tz=timezone.utc)


def _utc_now_iso() -> str:
    return _utc_now().isoformat()


def _tenant_key(tenant_id: str, entity_id: str) -> str:
    return f"{tenant_id}:{entity_id}"


def _normalize_entity(entity_type: str, entity_id: str) -> str:
    return f"{entity_type}:{entity_id}"


def _redact_sensitive_mapping(values: Mapping[str, Any]) -> dict[str, Any]:
    redacted: dict[str, Any] = {}
    for key, value in values.items():
        key_text = str(key)
        if any(token in key_text.lower() for token in SECRET_FIELD_TOKENS):
            redacted[key_text] = "[REDACTED]"
        elif isinstance(value, Mapping):
            redacted[key_text] = _redact_sensitive_mapping(value)
        else:
            redacted[key_text] = value
    return redacted


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


PHASE4_ADVANCED_IDENTITY_FEATURES: tuple[AdvancedIdentityBoundaryFeature, ...] = (
    AdvancedIdentityBoundaryFeature("feat:f08-sso", "federation", ("FederationRegistry", "IdentityProvider", "FederatedSession"), ("issuer", "audience", "claim-normalization")),
    AdvancedIdentityBoundaryFeature("feat:f05-passwordless-authentication", "advanced-authentication", ("AdvancedAuthenticatorRegistry", "PasswordlessCredential", "AuthenticationChallenge"), ("challenge-replay", "credential-revocation")),
    AdvancedIdentityBoundaryFeature("feat:f06-mfa", "advanced-authentication", ("AdvancedAuthenticatorRegistry", "MfaFactor"), ("amr-validation", "step-up")),
    AdvancedIdentityBoundaryFeature("feat:f07-webauthn", "advanced-authentication", ("AdvancedAuthenticatorRegistry", "WebAuthnCredential"), ("algorithm-allowlist", "sign-count")),
    AdvancedIdentityBoundaryFeature("feat:f09-federation", "federation", ("FederationRegistry", "IdentityProvider"), ("provider-kind", "issuer", "audience")),
    AdvancedIdentityBoundaryFeature("feat:f10-social-login", "federation", ("FederationRegistry", "IdentityProvider"), ("social-provider", "claim-normalization")),
    AdvancedIdentityBoundaryFeature("feat:f11-device-identity", "nonhuman-identity", ("DeviceWorkloadIdentityRegistry", "DeviceIdentity"), ("tenant-scope", "revocation")),
    AdvancedIdentityBoundaryFeature("feat:f12-workload-identity", "nonhuman-identity", ("DeviceWorkloadIdentityRegistry", "WorkloadIdentity"), ("trust-domain", "credential-rotation")),
    AdvancedIdentityBoundaryFeature("feat:f15-rebac", "graph-authorization", ("RelationshipGraph", "GraphDecision"), ("bounded-depth", "tenant-scope")),
    AdvancedIdentityBoundaryFeature("feat:f17-policy-language", "policy-language", ("PolicyRegistry", "PolicyDefinition"), ("safe-language", "context-conditions")),
    AdvancedIdentityBoundaryFeature("feat:f18-policy-versioning", "policy-versioning", ("PolicyRegistry", "PolicyVersion"), ("promotion", "rollback", "compatibility")),
    AdvancedIdentityBoundaryFeature("feat:f21-access-decision-api", "access-decision", ("AccessDecisionRequest", "AccessDecisionResponse", "PolicyRegistry"), ("idempotency", "explanation")),
    AdvancedIdentityBoundaryFeature("feat:f22-graph-based-authorization", "graph-authorization", ("RelationshipGraph", "RelationshipTuple"), ("path-resolution", "deny-without-path")),
    AdvancedIdentityBoundaryFeature("feat:f23-relationship-modeling", "relationship-modeling", ("RelationshipDefinition", "RelationshipTuple"), ("subject-type-schema", "schema-versioning")),
    AdvancedIdentityBoundaryFeature("feat:f26-contextual-auth-time-location", "adaptive-authentication", ("AdaptiveContext", "AdaptiveDecision", "evaluate_adaptive_context"), ("time", "location", "device-posture")),
    AdvancedIdentityBoundaryFeature("feat:f35-anomaly-detection-auth", "auth-telemetry", ("AuthAnomalyDetector", "AuthTelemetryEvent", "AnomalySignal"), ("redaction", "step-up-signal")),
    AdvancedIdentityBoundaryFeature("feat:f46-trust-federation-graphs", "trust-graph", ("TrustFederationGraph", "TrustPath"), ("active-path", "revoked-edge")),
    AdvancedIdentityBoundaryFeature("feat:f47-cross-cloud-identity", "cross-cloud-identity", ("TrustFederationGraph", "WorkloadIdentity"), ("cloud-mapping", "workload-trust-domain")),
)


def phase4_advanced_identity_boundary_manifest() -> dict[str, dict[str, Any]]:
    return {
        feature.feature_id: {
            "category": feature.category,
            "runtime_objects": list(feature.runtime_objects),
            "guarded_capabilities": list(feature.guarded_capabilities),
        }
        for feature in PHASE4_ADVANCED_IDENTITY_FEATURES
    }


def phase4_advanced_identity_boundary_integrity() -> dict[str, Any]:
    manifest = phase4_advanced_identity_boundary_manifest()
    categories = {row["category"] for row in manifest.values()}
    runtime_objects = {
        runtime_object
        for row in manifest.values()
        for runtime_object in row["runtime_objects"]
    }
    failures: list[str] = []
    if len(manifest) != 18:
        failures.append("phase 4 advanced identity boundary must track exactly 18 feature rows")
    for required in (
        "advanced-authentication",
        "federation",
        "nonhuman-identity",
        "graph-authorization",
        "policy-language",
        "auth-telemetry",
        "trust-graph",
        "cross-cloud-identity",
    ):
        if required not in categories:
            failures.append(f"missing category {required}")
    for required_object in (
        "AdvancedAuthenticatorRegistry",
        "FederationRegistry",
        "DeviceWorkloadIdentityRegistry",
        "RelationshipGraph",
        "PolicyRegistry",
        "AuthAnomalyDetector",
        "TrustFederationGraph",
    ):
        if required_object not in runtime_objects:
            failures.append(f"missing runtime object {required_object}")
    return {
        "passed": not failures,
        "feature_count": len(manifest),
        "categories": sorted(categories),
        "failures": failures,
    }


def evaluate_adaptive_context(context: AdaptiveContext) -> AdaptiveDecision:
    reasons: list[str] = []
    risk_score = 0
    if not context.trusted_network:
        risk_score += 1
        reasons.append("untrusted network context")
    if not context.trusted_device:
        risk_score += 2
        reasons.append("unknown or unhealthy device posture")
    if context.local_hour < 6 or context.local_hour > 22:
        risk_score += 1
        reasons.append("outside normal operating hours")
    if context.known_countries and context.ip_country not in context.known_countries:
        risk_score += 2
        reasons.append("unrecognized location")
    if context.anomaly_detected:
        risk_score += 2
        reasons.append("upstream anomaly signal present")

    if risk_score >= 5:
        return AdaptiveDecision(
            allowed=False,
            step_up_required=True,
            risk_level="high",
            reasons=tuple(reasons or ("bounded contextual risk threshold exceeded",)),
            amr=("mfa", "rba"),
        )
    if risk_score >= 2:
        return AdaptiveDecision(
            allowed=True,
            step_up_required=True,
            risk_level="medium",
            reasons=tuple(reasons or ("adaptive step-up required",)),
            amr=("mfa", "rba"),
        )
    return AdaptiveDecision(
        allowed=True,
        step_up_required=False,
        risk_level="low",
        reasons=tuple(reasons or ("context accepted within bounded policy",)),
        amr=("pwd",),
    )


class AdvancedAuthenticatorRegistry:
    def __init__(self) -> None:
        self._passwordless_credentials: dict[str, PasswordlessCredential] = {}
        self._mfa_factors: dict[str, MfaFactor] = {}
        self._webauthn_credentials: dict[str, WebAuthnCredential] = {}
        self._challenges: dict[str, AuthenticationChallenge] = {}

    @property
    def passwordless_credentials(self) -> Mapping[str, PasswordlessCredential]:
        return dict(self._passwordless_credentials)

    @property
    def mfa_factors(self) -> Mapping[str, MfaFactor]:
        return dict(self._mfa_factors)

    @property
    def webauthn_credentials(self) -> Mapping[str, WebAuthnCredential]:
        return dict(self._webauthn_credentials)

    def enroll_passwordless_credential(
        self,
        *,
        subject_id: str,
        tenant_id: str,
        credential_kind: str = "magic-link",
        recovery_codes: Iterable[str] = (),
    ) -> PasswordlessCredential:
        credential = PasswordlessCredential(
            credential_id=f"pwdless-{uuid4().hex}",
            subject_id=subject_id,
            tenant_id=tenant_id,
            credential_kind=credential_kind,
            recovery_codes=tuple(sorted(set(recovery_codes))),
            created_at=_utc_now_iso(),
        )
        self._passwordless_credentials[credential.credential_id] = credential
        return credential

    def revoke_passwordless_credential(self, credential_id: str) -> PasswordlessCredential:
        credential = self._passwordless_credentials[credential_id]
        updated = replace(credential, revoked=True)
        self._passwordless_credentials[credential_id] = updated
        return updated

    def register_webauthn_credential(
        self,
        *,
        subject_id: str,
        tenant_id: str,
        rp_id: str,
        algorithm: str,
        transports: Iterable[str] = (),
    ) -> WebAuthnCredential:
        if not is_webauthn_algorithm(algorithm):
            raise ValueError(f"unsupported WebAuthn algorithm {algorithm!r}")
        credential = WebAuthnCredential(
            credential_id=f"webauthn-{uuid4().hex}",
            subject_id=subject_id,
            tenant_id=tenant_id,
            rp_id=rp_id,
            algorithm=algorithm.upper(),
            transports=tuple(sorted(set(transports))),
            created_at=_utc_now_iso(),
        )
        self._webauthn_credentials[credential.credential_id] = credential
        return credential

    def revoke_webauthn_credential(self, credential_id: str) -> WebAuthnCredential:
        credential = self._webauthn_credentials[credential_id]
        updated = replace(credential, revoked=True)
        self._webauthn_credentials[credential_id] = updated
        return updated

    def enroll_mfa_factor(
        self,
        *,
        subject_id: str,
        tenant_id: str,
        method: str,
        bound_credential_id: str | None = None,
    ) -> MfaFactor:
        if not validate_amr_claim((method,)):
            raise ValueError(f"unsupported MFA method {method!r}")
        factor = MfaFactor(
            factor_id=f"mfa-{uuid4().hex}",
            subject_id=subject_id,
            tenant_id=tenant_id,
            method=method,
            created_at=_utc_now_iso(),
            bound_credential_id=bound_credential_id,
        )
        self._mfa_factors[factor.factor_id] = factor
        return factor

    def revoke_mfa_factor(self, factor_id: str) -> MfaFactor:
        factor = self._mfa_factors[factor_id]
        updated = replace(factor, revoked=True)
        self._mfa_factors[factor_id] = updated
        return updated

    def begin_passwordless_assertion(
        self,
        *,
        subject_id: str,
        tenant_id: str,
        context: AdaptiveContext,
    ) -> tuple[AuthenticationChallenge, AdaptiveDecision]:
        decision = evaluate_adaptive_context(context)
        allowed_methods = {"passwordless"}
        if any(
            credential.subject_id == subject_id
            and credential.tenant_id == tenant_id
            and not credential.revoked
            for credential in self._webauthn_credentials.values()
        ):
            allowed_methods.add("webauthn")
        if decision.step_up_required:
            allowed_methods.update(
                factor.method
                for factor in self._mfa_factors.values()
                if factor.subject_id == subject_id and factor.tenant_id == tenant_id and not factor.revoked
            )
        challenge = AuthenticationChallenge(
            challenge_id=f"challenge-{uuid4().hex}",
            subject_id=subject_id,
            tenant_id=tenant_id,
            challenge_kind="passwordless",
            expected_nonce=uuid4().hex,
            issued_at=_utc_now_iso(),
            expires_at=(_utc_now() + timedelta(minutes=5)).isoformat(),
            allowed_methods=tuple(sorted(allowed_methods)),
            step_up_required=decision.step_up_required,
        )
        self._challenges[challenge.challenge_id] = challenge
        return challenge, decision

    def complete_passwordless_assertion(
        self,
        *,
        challenge_id: str,
        credential_id: str,
        nonce: str,
    ) -> AuthenticationChallenge:
        challenge = self._challenges[challenge_id]
        if challenge.consumed:
            raise PermissionError("authentication challenge already consumed")
        if nonce != challenge.expected_nonce:
            raise PermissionError("authentication challenge nonce mismatch")
        if credential_id in self._webauthn_credentials:
            credential = self._webauthn_credentials[credential_id]
            if credential.revoked:
                raise PermissionError("webauthn credential is revoked")
            if credential.subject_id != challenge.subject_id or credential.tenant_id != challenge.tenant_id:
                raise PermissionError("webauthn credential subject mismatch")
            self._webauthn_credentials[credential_id] = replace(
                credential,
                sign_count=credential.sign_count + 1,
            )
        else:
            credential = self._passwordless_credentials.get(credential_id)
            if credential is None or credential.revoked:
                raise PermissionError("passwordless credential is inactive")
            if credential.subject_id != challenge.subject_id or credential.tenant_id != challenge.tenant_id:
                raise PermissionError("passwordless credential subject mismatch")
        completed = replace(challenge, consumed=True, bound_credential_id=credential_id)
        self._challenges[challenge_id] = completed
        return completed

    def begin_mfa_challenge(self, *, subject_id: str, tenant_id: str) -> AuthenticationChallenge:
        methods = sorted(
            factor.method
            for factor in self._mfa_factors.values()
            if factor.subject_id == subject_id and factor.tenant_id == tenant_id and not factor.revoked
        )
        if not methods:
            raise PermissionError("no active MFA factor available")
        challenge = AuthenticationChallenge(
            challenge_id=f"challenge-{uuid4().hex}",
            subject_id=subject_id,
            tenant_id=tenant_id,
            challenge_kind="mfa",
            expected_nonce=uuid4().hex,
            issued_at=_utc_now_iso(),
            expires_at=(_utc_now() + timedelta(minutes=5)).isoformat(),
            allowed_methods=tuple(methods),
            step_up_required=True,
        )
        self._challenges[challenge.challenge_id] = challenge
        return challenge

    def complete_mfa_challenge(
        self,
        *,
        challenge_id: str,
        factor_id: str,
        method: str,
        nonce: str,
    ) -> AuthenticationChallenge:
        challenge = self._challenges[challenge_id]
        if challenge.challenge_kind != "mfa":
            raise PermissionError("challenge kind mismatch")
        if challenge.consumed:
            raise PermissionError("mfa challenge already consumed")
        if nonce != challenge.expected_nonce:
            raise PermissionError("mfa challenge nonce mismatch")
        factor = self._mfa_factors[factor_id]
        if factor.revoked or factor.method != method:
            raise PermissionError("mfa factor is inactive")
        if factor.subject_id != challenge.subject_id or factor.tenant_id != challenge.tenant_id:
            raise PermissionError("mfa factor subject mismatch")
        completed = replace(challenge, consumed=True, bound_credential_id=factor_id)
        self._challenges[challenge_id] = completed
        return completed

    def summary(self) -> dict[str, Any]:
        return {
            "passwordless_credential_count": len(self._passwordless_credentials),
            "webauthn_credential_count": len(self._webauthn_credentials),
            "mfa_factor_count": len(self._mfa_factors),
            "active_passwordless_credentials": sum(
                not credential.revoked for credential in self._passwordless_credentials.values()
            ),
            "active_webauthn_credentials": sum(
                not credential.revoked for credential in self._webauthn_credentials.values()
            ),
            "active_mfa_factors": sum(not factor.revoked for factor in self._mfa_factors.values()),
        }


class FederationRegistry:
    def __init__(self) -> None:
        self._providers: dict[str, IdentityProvider] = {}
        self._sessions: dict[str, FederatedSession] = {}

    @property
    def providers(self) -> Mapping[str, IdentityProvider]:
        return dict(self._providers)

    def register_provider(
        self,
        *,
        provider_id: str,
        tenant_id: str,
        kind: str,
        issuer: str,
        discovery_url: str,
        audience: str,
        display_name: str,
        logout_supported: bool = False,
        claim_mapping: Mapping[str, str] | None = None,
        scopes: Iterable[str] = (),
    ) -> IdentityProvider:
        if kind not in {"social", "sso", "federation"}:
            raise ValueError(f"unsupported provider kind {kind!r}")
        provider = IdentityProvider(
            provider_id=provider_id,
            tenant_id=tenant_id,
            kind=kind,
            issuer=issuer,
            discovery_url=discovery_url,
            audience=audience,
            logout_supported=logout_supported,
            display_name=display_name,
            claim_mapping=dict(claim_mapping or {"sub": "sub", "email": "email", "name": "name"}),
            scopes=tuple(sorted(set(scopes))),
        )
        self._providers[provider_id] = provider
        return provider

    def rotate_provider_keys(self, provider_id: str) -> IdentityProvider:
        provider = self._providers[provider_id]
        updated = replace(provider, key_set_version=provider.key_set_version + 1)
        self._providers[provider_id] = updated
        return updated

    def normalize_claims(self, provider_id: str, claims: Mapping[str, Any]) -> dict[str, Any]:
        provider = self._providers[provider_id]
        normalized: dict[str, Any] = {"iss": provider.issuer}
        for target, source in provider.claim_mapping.items():
            normalized[target] = claims.get(source)
        if normalized.get("name") in {None, ""}:
            normalized["name"] = normalized.get("email") or normalized.get("sub")
        return normalized

    def bind_session(
        self,
        *,
        provider_id: str,
        tenant_id: str,
        session_id: str,
        issuer: str,
        audience: str,
        claims: Mapping[str, Any],
    ) -> FederatedSession:
        provider = self._providers[provider_id]
        if not provider.enabled:
            raise PermissionError("identity provider is disabled")
        if provider.tenant_id != tenant_id:
            raise PermissionError("identity provider tenant mismatch")
        if provider.issuer != issuer:
            raise PermissionError("identity provider issuer mismatch")
        if provider.audience != audience:
            raise PermissionError("identity provider audience mismatch")
        session = FederatedSession(
            session_id=session_id,
            provider_id=provider_id,
            tenant_id=tenant_id,
            issuer=issuer,
            audience=audience,
            logout_supported=provider.logout_supported,
            normalized_claims=self.normalize_claims(provider_id, claims),
            bound_at=_utc_now_iso(),
        )
        self._sessions[session_id] = session
        return session

    def summary(self) -> dict[str, Any]:
        return {
            "provider_count": len(self._providers),
            "active_provider_count": sum(provider.enabled for provider in self._providers.values()),
            "kinds": sorted({provider.kind for provider in self._providers.values()}),
            "session_count": len(self._sessions),
        }


class DeviceWorkloadIdentityRegistry:
    def __init__(self) -> None:
        self._devices: dict[str, DeviceIdentity] = {}
        self._workloads: dict[str, WorkloadIdentity] = {}

    @property
    def devices(self) -> Mapping[str, DeviceIdentity]:
        return dict(self._devices)

    @property
    def workloads(self) -> Mapping[str, WorkloadIdentity]:
        return dict(self._workloads)

    def register_device(
        self,
        *,
        device_id: str,
        subject_id: str,
        tenant_id: str,
        credential_posture: str,
        last_ip_country: str | None = None,
    ) -> DeviceIdentity:
        identity = DeviceIdentity(
            device_id=device_id,
            subject_id=subject_id,
            tenant_id=tenant_id,
            credential_posture=credential_posture,
            last_ip_country=last_ip_country,
            created_at=_utc_now_iso(),
        )
        self._devices[_tenant_key(tenant_id, device_id)] = identity
        return identity

    def revoke_device(self, *, device_id: str, tenant_id: str) -> DeviceIdentity:
        key = _tenant_key(tenant_id, device_id)
        identity = self._devices[key]
        updated = replace(identity, revoked=True)
        self._devices[key] = updated
        return updated

    def register_workload(
        self,
        *,
        workload_id: str,
        tenant_id: str,
        trust_domain: str,
        cloud: str,
        namespace: str,
        attestor: str,
    ) -> WorkloadIdentity:
        identity = WorkloadIdentity(
            workload_id=workload_id,
            tenant_id=tenant_id,
            trust_domain=trust_domain,
            cloud=cloud,
            namespace=namespace,
            attestor=attestor,
            credential_id=f"spire://{trust_domain}/{workload_id}/{uuid4().hex}",
            created_at=_utc_now_iso(),
        )
        self._workloads[_tenant_key(tenant_id, workload_id)] = identity
        return identity

    def rotate_workload_credential(self, *, workload_id: str, tenant_id: str) -> WorkloadIdentity:
        key = _tenant_key(tenant_id, workload_id)
        identity = self._workloads[key]
        updated = replace(identity, credential_id=f"spire://{identity.trust_domain}/{workload_id}/{uuid4().hex}")
        self._workloads[key] = updated
        return updated

    def revoke_workload(self, *, workload_id: str, tenant_id: str) -> WorkloadIdentity:
        key = _tenant_key(tenant_id, workload_id)
        identity = self._workloads[key]
        updated = replace(identity, revoked=True)
        self._workloads[key] = updated
        return updated

    def summary(self) -> dict[str, Any]:
        return {
            "device_count": len(self._devices),
            "active_device_count": sum(not device.revoked for device in self._devices.values()),
            "workload_count": len(self._workloads),
            "active_workload_count": sum(not workload.revoked for workload in self._workloads.values()),
            "trust_domains": sorted({workload.trust_domain for workload in self._workloads.values()}),
        }


class RelationshipGraph:
    def __init__(self) -> None:
        self._definitions: dict[tuple[str, str], RelationshipDefinition] = {}
        self._tuples: list[RelationshipTuple] = []

    @property
    def definitions(self) -> Mapping[tuple[str, str], RelationshipDefinition]:
        return dict(self._definitions)

    @property
    def tuples(self) -> tuple[RelationshipTuple, ...]:
        return tuple(self._tuples)

    def define_relation(
        self,
        *,
        resource_type: str,
        relation: str,
        subject_types: Iterable[str],
    ) -> RelationshipDefinition:
        key = (resource_type, relation)
        prior = self._definitions.get(key)
        definition = RelationshipDefinition(
            resource_type=resource_type,
            relation=relation,
            subject_types=tuple(sorted(set(subject_types))),
            version=1 if prior is None else prior.version + 1,
        )
        self._definitions[key] = definition
        return definition

    def add_tuple(
        self,
        *,
        resource_type: str,
        resource_id: str,
        relation: str,
        subject_type: str,
        subject_id: str,
        tenant_id: str,
    ) -> RelationshipTuple:
        definition = self._definitions[(resource_type, relation)]
        if subject_type not in definition.subject_types:
            raise ValueError("relationship subject type is not allowed by schema")
        relationship = RelationshipTuple(
            resource=_normalize_entity(resource_type, resource_id),
            relation=relation,
            subject=_normalize_entity(subject_type, subject_id),
            tenant_id=tenant_id,
        )
        self._tuples.append(relationship)
        return relationship

    def check_access(
        self,
        *,
        tenant_id: str,
        subject: str,
        relation: str,
        resource: str,
        max_depth: int = 5,
    ) -> GraphDecision:
        queue: deque[tuple[str, int, tuple[str, ...]]] = deque(
            (tuple_.subject, 1, (f"{tuple_.resource}#{tuple_.relation}@{tuple_.subject}",))
            for tuple_ in self._tuples
            if tuple_.tenant_id == tenant_id and tuple_.resource == resource and tuple_.relation == relation
        )
        seen: set[tuple[str, int]] = set()
        while queue:
            candidate_subject, depth, explanation = queue.popleft()
            if candidate_subject == subject:
                return GraphDecision(True, "relationship tuple grants access", explanation)
            if depth >= max_depth or (candidate_subject, depth) in seen:
                continue
            seen.add((candidate_subject, depth))
            for tuple_ in self._tuples:
                if tuple_.tenant_id != tenant_id:
                    continue
                if tuple_.resource == candidate_subject and tuple_.relation == "member":
                    queue.append(
                        (
                            tuple_.subject,
                            depth + 1,
                            explanation + (f"{tuple_.resource}#{tuple_.relation}@{tuple_.subject}",),
                        )
                    )
        return GraphDecision(False, "no bounded relationship path grants access", ())


class PolicyRegistry:
    def __init__(self, *, relationship_graph: RelationshipGraph) -> None:
        self.relationship_graph = relationship_graph
        self._definitions: dict[str, PolicyDefinition] = {}
        self._versions: dict[str, PolicyVersion] = {}
        self._versions_by_policy: dict[str, list[str]] = {}
        self._active_version_by_policy: dict[str, str] = {}

    @property
    def definitions(self) -> Mapping[str, PolicyDefinition]:
        return dict(self._definitions)

    @property
    def versions(self) -> Mapping[str, PolicyVersion]:
        return dict(self._versions)

    def create_policy(self, *, tenant_id: str, name: str, language: str = "tigrbl-conditions/v1") -> PolicyDefinition:
        if language != "tigrbl-conditions/v1":
            raise ValueError("unsupported policy language")
        definition = PolicyDefinition(
            policy_id=f"policy-{uuid4().hex}",
            name=name,
            tenant_id=tenant_id,
            language=language,
            created_at=_utc_now_iso(),
        )
        self._definitions[definition.policy_id] = definition
        self._versions_by_policy[definition.policy_id] = []
        return definition

    def publish_version(self, *, policy_id: str, source: str, promote: bool = True) -> PolicyVersion:
        definition = self._definitions[policy_id]
        relation, context_equals = self._parse_policy_source(source)
        current_ids = self._versions_by_policy[policy_id]
        version = PolicyVersion(
            version_id=f"policy-version-{uuid4().hex}",
            policy_id=policy_id,
            version_number=len(current_ids) + 1,
            source=source,
            created_at=_utc_now_iso(),
            relation=relation,
            context_equals=context_equals,
            promoted=False,
        )
        self._versions[version.version_id] = version
        current_ids.append(version.version_id)
        if promote:
            self.promote_version(version.version_id)
        return self._versions[version.version_id]

    def promote_version(self, version_id: str) -> PolicyVersion:
        version = self._versions[version_id]
        policy_id = version.policy_id
        for prior_id in self._versions_by_policy[policy_id]:
            prior = self._versions[prior_id]
            self._versions[prior_id] = replace(prior, promoted=False)
        updated = replace(version, promoted=True)
        self._versions[version_id] = updated
        self._active_version_by_policy[policy_id] = version_id
        return updated

    def rollback_policy(self, *, policy_id: str, version_id: str) -> PolicyVersion:
        if version_id not in self._versions_by_policy[policy_id]:
            raise KeyError("policy version does not belong to policy")
        return self.promote_version(version_id)

    def check_compatibility(self, *, left_version_id: str, right_version_id: str) -> bool:
        left = self._versions[left_version_id]
        right = self._versions[right_version_id]
        return left.relation == right.relation and set(left.context_equals).issubset(set(right.context_equals))

    def access_decision(self, request: AccessDecisionRequest) -> AccessDecisionResponse:
        policy_version = self._resolve_version(request)
        graph_decision = self.relationship_graph.check_access(
            tenant_id=request.tenant_id,
            subject=request.subject,
            relation=policy_version.relation,
            resource=request.resource,
        )
        if not graph_decision.allowed:
            return AccessDecisionResponse(
                allowed=False,
                reason=graph_decision.reason,
                correlation_id=request.correlation_id,
                policy_version_id=policy_version.version_id,
                explanation=graph_decision.explanation,
                idempotency_key=f"{request.correlation_id}:{request.subject}:{request.action}:{request.resource}",
            )
        missing_context = [
            key for key, _value in policy_version.context_equals
            if key not in request.context
        ]
        if missing_context:
            return AccessDecisionResponse(
                allowed=False,
                reason="required policy context is missing",
                correlation_id=request.correlation_id,
                policy_version_id=policy_version.version_id,
                explanation=tuple(missing_context),
                idempotency_key=f"{request.correlation_id}:{request.subject}:{request.action}:{request.resource}",
            )
        mismatched_context = [
            key for key, expected_value in policy_version.context_equals
            if request.context[key] != expected_value
        ]
        if mismatched_context:
            return AccessDecisionResponse(
                allowed=False,
                reason="policy context does not satisfy required values",
                correlation_id=request.correlation_id,
                policy_version_id=policy_version.version_id,
                explanation=tuple(mismatched_context),
                idempotency_key=f"{request.correlation_id}:{request.subject}:{request.action}:{request.resource}",
            )
        return AccessDecisionResponse(
            allowed=True,
            reason="policy version and relationship graph grant access",
            correlation_id=request.correlation_id,
            policy_version_id=policy_version.version_id,
            explanation=graph_decision.explanation + tuple(
                f"context.{key}={request.context[key]!r}" for key, _value in policy_version.context_equals
            ),
            idempotency_key=f"{request.correlation_id}:{request.subject}:{request.action}:{request.resource}",
        )

    def _resolve_version(self, request: AccessDecisionRequest) -> PolicyVersion:
        if request.policy_version_id is not None:
            return self._versions[request.policy_version_id]
        for policy_id, definition in self._definitions.items():
            if definition.tenant_id == request.tenant_id and definition.name == request.action:
                active_version_id = self._active_version_by_policy[policy_id]
                return self._versions[active_version_id]
        raise KeyError(f"no active policy found for action {request.action!r}")

    def _parse_policy_source(self, source: str) -> tuple[str, tuple[tuple[str, Any], ...]]:
        normalized = " ".join(source.strip().split())
        if not normalized.startswith("allow if relation "):
            raise ValueError("policy must start with 'allow if relation <name>'")
        if any(token in normalized for token in ("import ", "exec", "lambda", ";", "__")):
            raise ValueError("unsafe construct detected in policy source")
        fragments = [fragment.strip() for fragment in normalized.split(" and ")]
        relation_fragment = fragments[0]
        relation = relation_fragment.removeprefix("allow if relation ").strip()
        if not relation:
            raise ValueError("policy relation is required")
        context_equals: list[tuple[str, Any]] = []
        for fragment in fragments[1:]:
            if not fragment.startswith("context.") or "==" not in fragment:
                raise ValueError("policy conditions must be 'context.<field> == <value>'")
            field, raw_value = [part.strip() for part in fragment.split("==", 1)]
            field = field.replace("context.", "").strip()
            if not field:
                raise ValueError("policy context field is required")
            if raw_value in {"true", "false"}:
                parsed_value: Any = raw_value == "true"
            elif raw_value.startswith('"') and raw_value.endswith('"'):
                parsed_value = raw_value[1:-1]
            else:
                try:
                    parsed_value = int(raw_value)
                except ValueError:
                    parsed_value = raw_value
            context_equals.append((field, parsed_value))
        return relation, tuple(context_equals)


class AuthAnomalyDetector:
    def __init__(self) -> None:
        self._events: list[AuthTelemetryEvent] = []

    @property
    def events(self) -> tuple[AuthTelemetryEvent, ...]:
        return tuple(self._events)

    def record_event(
        self,
        *,
        tenant_id: str,
        subject_id: str,
        event_type: str,
        correlation_id: str,
        ip_country: str,
        trusted_device: bool,
        outcome: str,
        details: Mapping[str, Any],
    ) -> tuple[AuthTelemetryEvent, AnomalySignal | None]:
        event = AuthTelemetryEvent(
            event_id=f"auth-event-{uuid4().hex}",
            tenant_id=tenant_id,
            subject_id=subject_id,
            event_type=event_type,
            correlation_id=correlation_id,
            ip_country=ip_country,
            trusted_device=trusted_device,
            outcome=outcome,
            details=_redact_sensitive_mapping(details),
            recorded_at=_utc_now_iso(),
        )
        self._events.append(event)
        return event, self._detect_signal(event)

    def _detect_signal(self, event: AuthTelemetryEvent) -> AnomalySignal | None:
        reasons: list[str] = []
        previous_countries = {
            item.ip_country
            for item in self._events[:-1]
            if item.tenant_id == event.tenant_id and item.subject_id == event.subject_id
        }
        failure_count = sum(
            1
            for item in self._events
            if item.tenant_id == event.tenant_id and item.subject_id == event.subject_id and item.outcome == "failure"
        )
        if previous_countries and event.ip_country not in previous_countries:
            reasons.append("impossible travel or first-seen country")
        if not event.trusted_device:
            reasons.append("untrusted device telemetry")
        if failure_count >= 3:
            reasons.append("repeated authentication failures")
        if not reasons:
            return None
        severity = "high" if len(reasons) >= 3 else "medium"
        return AnomalySignal(
            signal_id=f"anomaly-{uuid4().hex}",
            tenant_id=event.tenant_id,
            subject_id=event.subject_id,
            correlation_id=event.correlation_id,
            severity=severity,
            reasons=tuple(reasons),
            recommended_action="step_up" if severity == "medium" else "manual-review",
            redacted_details=event.details,
        )

    def summary(self) -> dict[str, Any]:
        return {
            "event_count": len(self._events),
            "tenant_ids": sorted({event.tenant_id for event in self._events}),
        }


class TrustFederationGraph:
    def __init__(self) -> None:
        self._domains: dict[str, TrustDomain] = {}
        self._edges: list[TrustEdge] = []

    @property
    def domains(self) -> Mapping[str, TrustDomain]:
        return dict(self._domains)

    @property
    def edges(self) -> tuple[TrustEdge, ...]:
        return tuple(self._edges)

    def add_domain(self, *, name: str, issuers: Iterable[str], clouds: Iterable[str]) -> TrustDomain:
        domain = TrustDomain(
            name=name,
            issuers=tuple(sorted(set(issuers))),
            clouds=tuple(sorted(set(clouds))),
        )
        self._domains[name] = domain
        return domain

    def add_edge(
        self,
        *,
        source_domain: str,
        target_domain: str,
        exchange_kind: str,
        constraints: Mapping[str, Any],
    ) -> TrustEdge:
        if source_domain not in self._domains or target_domain not in self._domains:
            raise KeyError("trust domains must exist before adding an edge")
        edge = TrustEdge(
            source_domain=source_domain,
            target_domain=target_domain,
            exchange_kind=exchange_kind,
            constraints=dict(constraints),
        )
        self._edges.append(edge)
        return edge

    def revoke_edge(self, *, source_domain: str, target_domain: str) -> TrustEdge:
        for index, edge in enumerate(self._edges):
            if edge.source_domain == source_domain and edge.target_domain == target_domain and not edge.revoked:
                updated = replace(edge, revoked=True)
                self._edges[index] = updated
                return updated
        raise KeyError("trust edge not found")

    def resolve_path(self, *, source_domain: str, target_domain: str, max_hops: int = 5) -> TrustPath:
        queue: deque[tuple[str, tuple[str, ...], tuple[str, ...]]] = deque(
            [(source_domain, (), (source_domain,))]
        )
        seen: set[str] = set()
        while queue:
            current, exchange_kinds, hops = queue.popleft()
            if current == target_domain:
                return TrustPath(
                    source_domain=source_domain,
                    target_domain=target_domain,
                    hops=hops,
                    exchange_kinds=exchange_kinds,
                )
            if current in seen or len(hops) > max_hops:
                continue
            seen.add(current)
            for edge in self._edges:
                if edge.revoked or edge.source_domain != current:
                    continue
                queue.append(
                    (
                        edge.target_domain,
                        exchange_kinds + (edge.exchange_kind,),
                        hops + (edge.target_domain,),
                    )
                )
        raise PermissionError("no active trust path found")

    def map_cross_cloud_workload(
        self,
        *,
        workload: WorkloadIdentity,
        target_domain: str,
    ) -> dict[str, Any]:
        path = self.resolve_path(source_domain=workload.trust_domain, target_domain=target_domain)
        target = self._domains[target_domain]
        return {
            "workload_id": workload.workload_id,
            "source_domain": workload.trust_domain,
            "target_domain": target_domain,
            "source_cloud": workload.cloud,
            "target_clouds": list(target.clouds),
            "path": list(path.hops),
            "exchange_kinds": list(path.exchange_kinds),
        }


def build_phase4_delivery_summary(
    *,
    authenticator_registry: AdvancedAuthenticatorRegistry,
    federation_registry: FederationRegistry,
    device_workload_registry: DeviceWorkloadIdentityRegistry,
    relationship_graph: RelationshipGraph,
    policy_registry: PolicyRegistry,
    anomaly_detector: AuthAnomalyDetector,
    trust_graph: TrustFederationGraph,
) -> dict[str, Any]:
    return {
        "advanced_authentication": authenticator_registry.summary(),
        "federation": federation_registry.summary(),
        "non_human_identities": device_workload_registry.summary(),
        "relationship_graph": {
            "definition_count": len(relationship_graph.definitions),
            "tuple_count": len(relationship_graph.tuples),
        },
        "policy_control_plane": {
            "policy_count": len(policy_registry.definitions),
            "policy_version_count": len(policy_registry.versions),
            "active_policy_count": len({version.policy_id for version in policy_registry.versions.values() if version.promoted}),
        },
        "anomaly_detection": anomaly_detector.summary(),
        "trust_graph": {
            "domain_count": len(trust_graph.domains),
            "edge_count": len(trust_graph.edges),
        },
    }


__all__ = [
    "AccessDecisionRequest",
    "AccessDecisionResponse",
    "AdaptiveContext",
    "AdaptiveDecision",
    "AdvancedIdentityBoundaryFeature",
    "AdvancedAuthenticatorRegistry",
    "AnomalySignal",
    "AuthAnomalyDetector",
    "AuthTelemetryEvent",
    "AuthenticationChallenge",
    "DeviceIdentity",
    "DeviceWorkloadIdentityRegistry",
    "FederatedSession",
    "FederationRegistry",
    "GraphDecision",
    "IdentityProvider",
    "MfaFactor",
    "PasswordlessCredential",
    "PolicyDefinition",
    "PolicyRegistry",
    "PolicyVersion",
    "PHASE4_ADVANCED_IDENTITY_FEATURES",
    "RelationshipDefinition",
    "RelationshipGraph",
    "RelationshipTuple",
    "TrustDomain",
    "TrustEdge",
    "TrustFederationGraph",
    "TrustPath",
    "WebAuthnCredential",
    "WorkloadIdentity",
    "build_phase4_delivery_summary",
    "evaluate_adaptive_context",
    "phase4_advanced_identity_boundary_integrity",
    "phase4_advanced_identity_boundary_manifest",
]
