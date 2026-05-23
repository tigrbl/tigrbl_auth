from __future__ import annotations

import pytest

from tigrbl_auth.services.advanced_identity_plane import (
    AccessDecisionRequest,
    AdaptiveContext,
    AdvancedAuthenticatorRegistry,
    AuthAnomalyDetector,
    DeviceWorkloadIdentityRegistry,
    FederationRegistry,
    PolicyRegistry,
    RelationshipGraph,
    TrustFederationGraph,
    build_phase4_delivery_summary,
    phase4_advanced_identity_boundary_integrity,
    phase4_advanced_identity_boundary_manifest,
)


BOUNDARY_FEATURE_IDS = {
    "feat:f08-sso",
    "feat:f05-passwordless-authentication",
    "feat:f06-mfa",
    "feat:f07-webauthn",
    "feat:f09-federation",
    "feat:f10-social-login",
    "feat:f11-device-identity",
    "feat:f12-workload-identity",
    "feat:f15-rebac",
    "feat:f17-policy-language",
    "feat:f18-policy-versioning",
    "feat:f21-access-decision-api",
    "feat:f22-graph-based-authorization",
    "feat:f23-relationship-modeling",
    "feat:f26-contextual-auth-time-location",
    "feat:f35-anomaly-detection-auth",
    "feat:f46-trust-federation-graphs",
    "feat:f47-cross-cloud-identity",
}


def _authenticators() -> AdvancedAuthenticatorRegistry:
    registry = AdvancedAuthenticatorRegistry()
    webauthn = registry.register_webauthn_credential(
        subject_id="alice",
        tenant_id="tenant-a",
        rp_id="auth.example.test",
        algorithm="ES256",
        transports=("internal",),
    )
    registry.enroll_passwordless_credential(
        subject_id="alice",
        tenant_id="tenant-a",
        credential_kind="magic-link",
    )
    registry.enroll_mfa_factor(
        subject_id="alice",
        tenant_id="tenant-a",
        method="otp",
        bound_credential_id=webauthn.credential_id,
    )
    return registry


def _federation() -> FederationRegistry:
    registry = FederationRegistry()
    registry.register_provider(
        provider_id="corp-sso",
        tenant_id="tenant-a",
        kind="sso",
        issuer="https://login.example.test",
        discovery_url="https://login.example.test/.well-known/openid-configuration",
        audience="public-uix",
        display_name="Example SSO",
        logout_supported=True,
        claim_mapping={"sub": "sub", "email": "mail", "name": "display_name"},
    )
    registry.register_provider(
        provider_id="github",
        tenant_id="tenant-a",
        kind="social",
        issuer="https://github.com/login/oauth",
        discovery_url="https://github.com/.well-known/openid-configuration",
        audience="public-uix",
        display_name="GitHub",
    )
    registry.register_provider(
        provider_id="partner",
        tenant_id="tenant-a",
        kind="federation",
        issuer="https://partner.example.test",
        discovery_url="https://partner.example.test/federation.json",
        audience="token-exchange",
        display_name="Partner Federation",
    )
    return registry


def _graph_and_policies() -> tuple[RelationshipGraph, PolicyRegistry]:
    graph = RelationshipGraph()
    graph.define_relation(resource_type="document", relation="viewer", subject_types=("group", "user"))
    graph.define_relation(resource_type="group", relation="member", subject_types=("group", "user"))
    graph.add_tuple(
        resource_type="document",
        resource_id="roadmap",
        relation="viewer",
        subject_type="group",
        subject_id="eng",
        tenant_id="tenant-a",
    )
    graph.add_tuple(
        resource_type="group",
        resource_id="eng",
        relation="member",
        subject_type="user",
        subject_id="alice",
        tenant_id="tenant-a",
    )
    policies = PolicyRegistry(relationship_graph=graph)
    policy = policies.create_policy(tenant_id="tenant-a", name="document.read")
    policies.publish_version(
        policy_id=policy.policy_id,
        source='allow if relation viewer and context.tenant == "tenant-a" and context.mfa == true',
    )
    return graph, policies


def _nonhuman_and_trust() -> tuple[DeviceWorkloadIdentityRegistry, TrustFederationGraph]:
    identities = DeviceWorkloadIdentityRegistry()
    identities.register_device(
        device_id="device-1",
        subject_id="alice",
        tenant_id="tenant-a",
        credential_posture="managed",
        last_ip_country="US",
    )
    identities.register_workload(
        workload_id="payments-api",
        tenant_id="tenant-a",
        trust_domain="spiffe://aws.example/payments",
        cloud="aws",
        namespace="payments",
        attestor="spire-agent",
    )
    trust = TrustFederationGraph()
    trust.add_domain(name="spiffe://aws.example/payments", issuers=("https://sts.aws.example",), clouds=("aws",))
    trust.add_domain(name="trust://hub.example", issuers=("https://hub.example",), clouds=("aws", "gcp"))
    trust.add_domain(name="spiffe://gcp.example/payments", issuers=("https://iam.gcp.example",), clouds=("gcp",))
    trust.add_edge(
        source_domain="spiffe://aws.example/payments",
        target_domain="trust://hub.example",
        exchange_kind="token-exchange",
        constraints={"audience": "hub"},
    )
    trust.add_edge(
        source_domain="trust://hub.example",
        target_domain="spiffe://gcp.example/payments",
        exchange_kind="federated-workload",
        constraints={"audience": "gcp"},
    )
    return identities, trust


def test_phase4_advanced_identity_boundary_t0_inventory_tracks_all_features():
    manifest = phase4_advanced_identity_boundary_manifest()
    integrity = phase4_advanced_identity_boundary_integrity()

    assert set(manifest) == BOUNDARY_FEATURE_IDS
    assert integrity["passed"] is True
    assert integrity["feature_count"] == 18
    assert "advanced-authentication" in integrity["categories"]
    assert "graph-authorization" in integrity["categories"]
    assert manifest["feat:f47-cross-cloud-identity"]["category"] == "cross-cloud-identity"


def test_phase4_advanced_identity_boundary_t1_composes_advanced_identity_runtime():
    authenticators = _authenticators()
    federation = _federation()
    nonhuman, trust = _nonhuman_and_trust()
    graph, policies = _graph_and_policies()
    detector = AuthAnomalyDetector()

    challenge, adaptive = authenticators.begin_passwordless_assertion(
        subject_id="alice",
        tenant_id="tenant-a",
        context=AdaptiveContext(
            tenant_id="tenant-a",
            trusted_network=False,
            trusted_device=False,
            ip_country="DE",
            local_hour=23,
            known_countries=("US", "DE"),
        ),
    )
    credential_id = next(iter(authenticators.webauthn_credentials))
    authenticators.complete_passwordless_assertion(
        challenge_id=challenge.challenge_id,
        credential_id=credential_id,
        nonce=challenge.expected_nonce,
    )
    session = federation.bind_session(
        provider_id="corp-sso",
        tenant_id="tenant-a",
        session_id="sess-1",
        issuer="https://login.example.test",
        audience="public-uix",
        claims={"sub": "alice", "mail": "alice@example.test", "display_name": "Alice"},
    )
    decision = policies.access_decision(
        AccessDecisionRequest(
            tenant_id="tenant-a",
            subject="user:alice",
            action="document.read",
            resource="document:roadmap",
            context={"tenant": "tenant-a", "mfa": True},
            correlation_id="corr-allow",
        )
    )
    detector.record_event(
        tenant_id="tenant-a",
        subject_id="alice",
        event_type="login",
        correlation_id="corr-allow",
        ip_country="US",
        trusted_device=True,
        outcome="success",
        details={"session_token": "secret"},
    )
    workload = nonhuman.rotate_workload_credential(workload_id="payments-api", tenant_id="tenant-a")
    mapping = trust.map_cross_cloud_workload(
        workload=workload,
        target_domain="spiffe://gcp.example/payments",
    )
    summary = build_phase4_delivery_summary(
        authenticator_registry=authenticators,
        federation_registry=federation,
        device_workload_registry=nonhuman,
        relationship_graph=graph,
        policy_registry=policies,
        anomaly_detector=detector,
        trust_graph=trust,
    )

    assert adaptive.step_up_required
    assert session.normalized_claims["email"] == "alice@example.test"
    assert decision.allowed
    assert mapping["target_clouds"] == ["gcp"]
    assert summary["advanced_authentication"]["active_webauthn_credentials"] == 1
    assert summary["federation"]["provider_count"] == 3
    assert summary["non_human_identities"]["active_workload_count"] == 1
    assert summary["policy_control_plane"]["active_policy_count"] == 1


def test_phase4_advanced_identity_boundary_t2_fails_closed_for_replay_policy_and_trust_drift():
    authenticators = _authenticators()
    federation = _federation()
    nonhuman, trust = _nonhuman_and_trust()
    graph, policies = _graph_and_policies()
    detector = AuthAnomalyDetector()

    challenge, _adaptive = authenticators.begin_passwordless_assertion(
        subject_id="alice",
        tenant_id="tenant-a",
        context=AdaptiveContext(
            tenant_id="tenant-a",
            trusted_network=True,
            trusted_device=True,
            ip_country="US",
            local_hour=10,
            known_countries=("US",),
        ),
    )
    credential_id = next(iter(authenticators.webauthn_credentials))
    authenticators.complete_passwordless_assertion(
        challenge_id=challenge.challenge_id,
        credential_id=credential_id,
        nonce=challenge.expected_nonce,
    )
    _, signal = detector.record_event(
        tenant_id="tenant-a",
        subject_id="alice",
        event_type="login",
        correlation_id="corr-risk",
        ip_country="DE",
        trusted_device=False,
        outcome="failure",
        details={"access_token": "secret"},
    )
    denied = policies.access_decision(
        AccessDecisionRequest(
            tenant_id="tenant-a",
            subject="user:alice",
            action="document.read",
            resource="document:roadmap",
            context={"tenant": "tenant-a", "mfa": False},
            correlation_id="corr-deny",
        )
    )
    no_path = graph.check_access(
        tenant_id="tenant-a",
        subject="user:bob",
        relation="viewer",
        resource="document:roadmap",
    )

    assert signal is not None
    assert signal.redacted_details["access_token"] == "[REDACTED]"
    assert denied.allowed is False
    assert denied.reason == "policy context does not satisfy required values"
    assert no_path.allowed is False

    revoked_challenge, _ = authenticators.begin_passwordless_assertion(
        subject_id="alice",
        tenant_id="tenant-a",
        context=AdaptiveContext(
            tenant_id="tenant-a",
            trusted_network=True,
            trusted_device=True,
            ip_country="US",
            local_hour=10,
        ),
    )
    authenticators.revoke_webauthn_credential(credential_id)
    with pytest.raises(PermissionError, match="webauthn credential is revoked"):
        authenticators.complete_passwordless_assertion(
            challenge_id=revoked_challenge.challenge_id,
            credential_id=credential_id,
            nonce=revoked_challenge.expected_nonce,
        )
    with pytest.raises(PermissionError, match="already consumed"):
        authenticators.complete_passwordless_assertion(
            challenge_id=challenge.challenge_id,
            credential_id=credential_id,
            nonce=challenge.expected_nonce,
        )
    with pytest.raises(ValueError, match="unsupported provider kind"):
        federation.register_provider(
            provider_id="bad",
            tenant_id="tenant-a",
            kind="saml",
            issuer="https://bad.example.test",
            discovery_url="https://bad.example.test/.well-known",
            audience="public-uix",
            display_name="Bad Provider",
        )
    with pytest.raises(PermissionError, match="issuer mismatch"):
        federation.bind_session(
            provider_id="corp-sso",
            tenant_id="tenant-a",
            session_id="bad-sess",
            issuer="https://evil.example.test",
            audience="public-uix",
            claims={"sub": "alice"},
        )
    policy = policies.create_policy(tenant_id="tenant-a", name="document.write")
    with pytest.raises(ValueError, match="unsafe construct"):
        policies.publish_version(
            policy_id=policy.policy_id,
            source='allow if relation viewer and context.tenant == "tenant-a"; exec',
        )
    trust.revoke_edge(
        source_domain="trust://hub.example",
        target_domain="spiffe://gcp.example/payments",
    )
    workload = nonhuman.workloads["tenant-a:payments-api"]
    with pytest.raises(PermissionError, match="no active trust path"):
        trust.map_cross_cloud_workload(
            workload=workload,
            target_domain="spiffe://gcp.example/payments",
        )
