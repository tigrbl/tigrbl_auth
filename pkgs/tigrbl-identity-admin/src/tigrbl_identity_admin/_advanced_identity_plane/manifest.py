from __future__ import annotations

from typing import Any

from .models import AdvancedIdentityBoundaryFeature


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
