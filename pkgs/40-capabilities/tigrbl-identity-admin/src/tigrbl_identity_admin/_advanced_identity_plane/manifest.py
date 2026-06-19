from __future__ import annotations

from typing import Any


ADVANCED_IDENTITY_GRAPH_AUTH_FEATURES: tuple[dict[str, Any], ...] = (
    {"feature_id": "feat:f08-sso", "category": "federation", "runtime_objects": ("FederationRegistry", "IdentityProvider", "FederatedSession"), "guarded_capabilities": ("issuer", "audience", "claim-normalization")},
    {"feature_id": "feat:f05-passwordless-authentication", "category": "advanced-authentication", "runtime_objects": ("AdvancedAuthenticatorRegistry", "PasswordlessCredential", "AuthenticationChallenge"), "guarded_capabilities": ("challenge-replay", "credential-revocation")},
    {"feature_id": "feat:f06-mfa", "category": "advanced-authentication", "runtime_objects": ("AdvancedAuthenticatorRegistry", "MfaFactor"), "guarded_capabilities": ("amr-validation", "step-up")},
    {"feature_id": "feat:f07-webauthn", "category": "advanced-authentication", "runtime_objects": ("AdvancedAuthenticatorRegistry", "WebAuthnCredential"), "guarded_capabilities": ("algorithm-allowlist", "sign-count")},
    {"feature_id": "feat:f09-federation", "category": "federation", "runtime_objects": ("FederationRegistry", "IdentityProvider"), "guarded_capabilities": ("provider-kind", "issuer", "audience")},
    {"feature_id": "feat:f10-social-login", "category": "federation", "runtime_objects": ("FederationRegistry", "IdentityProvider"), "guarded_capabilities": ("social-provider", "claim-normalization")},
    {"feature_id": "feat:f11-device-identity", "category": "nonhuman-identity", "runtime_objects": ("DeviceWorkloadIdentityRegistry", "DeviceIdentity"), "guarded_capabilities": ("tenant-scope", "revocation")},
    {"feature_id": "feat:f12-workload-identity", "category": "nonhuman-identity", "runtime_objects": ("DeviceWorkloadIdentityRegistry", "WorkloadIdentity"), "guarded_capabilities": ("trust-domain", "credential-rotation")},
    {"feature_id": "feat:f15-rebac", "category": "graph-authorization", "runtime_objects": ("RelationshipGraph", "GraphDecision"), "guarded_capabilities": ("bounded-depth", "tenant-scope")},
    {"feature_id": "feat:f17-policy-language", "category": "policy-language", "runtime_objects": ("PolicyRegistry", "PolicyDefinition"), "guarded_capabilities": ("safe-language", "context-conditions")},
    {"feature_id": "feat:f18-policy-versioning", "category": "policy-versioning", "runtime_objects": ("PolicyRegistry", "PolicyVersion"), "guarded_capabilities": ("promotion", "rollback", "compatibility")},
    {"feature_id": "feat:f21-access-decision-api", "category": "access-decision", "runtime_objects": ("AccessDecisionRequest", "AccessDecisionResponse", "PolicyRegistry"), "guarded_capabilities": ("idempotency", "explanation")},
    {"feature_id": "feat:f22-graph-based-authorization", "category": "graph-authorization", "runtime_objects": ("RelationshipGraph", "RelationshipTuple"), "guarded_capabilities": ("path-resolution", "deny-without-path")},
    {"feature_id": "feat:f23-relationship-modeling", "category": "relationship-modeling", "runtime_objects": ("RelationshipDefinition", "RelationshipTuple"), "guarded_capabilities": ("subject-type-schema", "schema-versioning")},
    {"feature_id": "feat:f26-contextual-auth-time-location", "category": "adaptive-authentication", "runtime_objects": ("AdaptiveContext", "AdaptiveDecision", "evaluate_adaptive_context"), "guarded_capabilities": ("time", "location", "device-posture")},
    {"feature_id": "feat:f35-anomaly-detection-auth", "category": "auth-telemetry", "runtime_objects": ("AuthAnomalyDetector", "AuthTelemetryEvent", "AnomalySignal"), "guarded_capabilities": ("redaction", "step-up-signal")},
    {"feature_id": "feat:f46-trust-federation-graphs", "category": "trust-graph", "runtime_objects": ("TrustFederationGraph", "TrustPath"), "guarded_capabilities": ("active-path", "revoked-edge")},
    {"feature_id": "feat:f47-cross-cloud-identity", "category": "cross-cloud-identity", "runtime_objects": ("TrustFederationGraph", "WorkloadIdentity"), "guarded_capabilities": ("cloud-mapping", "workload-trust-domain")},
)


def advanced_identity_graph_auth_boundary_manifest() -> dict[str, dict[str, Any]]:
    return {
        str(feature["feature_id"]): {
            "category": feature["category"],
            "runtime_objects": list(feature["runtime_objects"]),
            "guarded_capabilities": list(feature["guarded_capabilities"]),
        }
        for feature in ADVANCED_IDENTITY_GRAPH_AUTH_FEATURES
    }


def advanced_identity_graph_auth_boundary_integrity() -> dict[str, Any]:
    manifest = advanced_identity_graph_auth_boundary_manifest()
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


PHASE4_ADVANCED_IDENTITY_FEATURES = ADVANCED_IDENTITY_GRAPH_AUTH_FEATURES
phase4_advanced_identity_boundary_manifest = advanced_identity_graph_auth_boundary_manifest
phase4_advanced_identity_boundary_integrity = advanced_identity_graph_auth_boundary_integrity
