import pytest

from tigrbl_identity_admin_advanced_authenticator_registry import (
    AdvancedAuthenticatorRegistry as CanonicalAdvancedAuthenticatorRegistry,
)
from tigrbl_identity_admin_policy_registry import PolicyRegistry as CanonicalPolicyRegistry
from tigrbl_identity_admin_relationship_graph import RelationshipGraph as CanonicalRelationshipGraph
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
)


def test_advanced_authenticator_registry_supports_passwordless_webauthn_mfa_and_replay_safety():
    assert AdvancedAuthenticatorRegistry is CanonicalAdvancedAuthenticatorRegistry

    registry = AdvancedAuthenticatorRegistry()
    passwordless = registry.enroll_passwordless_credential(
        subject_id="alice",
        tenant_id="tenant-a",
        recovery_codes=("backup-1", "backup-2"),
    )
    webauthn = registry.register_webauthn_credential(
        subject_id="alice",
        tenant_id="tenant-a",
        rp_id="auth.example.com",
        algorithm="ES256",
        transports=("internal", "hybrid"),
    )
    factor = registry.enroll_mfa_factor(
        subject_id="alice",
        tenant_id="tenant-a",
        method="otp",
        bound_credential_id=webauthn.credential_id,
    )

    challenge, decision = registry.begin_passwordless_assertion(
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

    assert passwordless.recovery_codes == ("backup-1", "backup-2")
    assert decision.allowed
    assert decision.step_up_required
    assert decision.risk_level == "medium"
    assert set(challenge.allowed_methods) == {"otp", "passwordless", "webauthn"}

    completed = registry.complete_passwordless_assertion(
        challenge_id=challenge.challenge_id,
        credential_id=webauthn.credential_id,
        nonce=challenge.expected_nonce,
    )
    mfa_challenge = registry.begin_mfa_challenge(subject_id="alice", tenant_id="tenant-a")
    registry.complete_mfa_challenge(
        challenge_id=mfa_challenge.challenge_id,
        factor_id=factor.factor_id,
        method="otp",
        nonce=mfa_challenge.expected_nonce,
    )

    assert completed.bound_credential_id == webauthn.credential_id
    assert registry.webauthn_credentials[webauthn.credential_id].sign_count == 1

    with pytest.raises(PermissionError, match="already consumed"):
        registry.complete_passwordless_assertion(
            challenge_id=challenge.challenge_id,
            credential_id=webauthn.credential_id,
            nonce=challenge.expected_nonce,
        )


def test_federation_registry_supports_sso_social_provider_trust_claim_normalization_and_logout():
    registry = FederationRegistry()
    social = registry.register_provider(
        provider_id="github",
        tenant_id="tenant-a",
        kind="social",
        issuer="https://github.com/login/oauth",
        discovery_url="https://github.com/.well-known/openid-configuration",
        audience="public-uix",
        display_name="GitHub",
        scopes=("openid", "email"),
    )
    sso = registry.register_provider(
        provider_id="corp-sso",
        tenant_id="tenant-a",
        kind="sso",
        issuer="https://login.example.com",
        discovery_url="https://login.example.com/.well-known/openid-configuration",
        audience="public-uix",
        display_name="Contoso SSO",
        logout_supported=True,
        claim_mapping={"sub": "sub", "email": "mail", "name": "display_name"},
    )
    registry.register_provider(
        provider_id="partner-fed",
        tenant_id="tenant-a",
        kind="federation",
        issuer="https://partner.example.com",
        discovery_url="https://partner.example.com/federation.json",
        audience="token-exchange",
        display_name="Partner Federation",
    )
    rotated = registry.rotate_provider_keys("corp-sso")
    session = registry.bind_session(
        provider_id="corp-sso",
        tenant_id="tenant-a",
        session_id="session-1",
        issuer="https://login.example.com",
        audience="public-uix",
        claims={"sub": "alice", "mail": "alice@example.com", "display_name": "Alice"},
    )

    assert social.kind == "social"
    assert rotated.key_set_version == 2
    assert session.logout_supported
    assert session.normalized_claims["email"] == "alice@example.com"
    assert session.normalized_claims["name"] == "Alice"

    with pytest.raises(PermissionError, match="issuer mismatch"):
        registry.bind_session(
            provider_id="corp-sso",
            tenant_id="tenant-a",
            session_id="session-2",
            issuer="https://evil.example.com",
            audience="public-uix",
            claims={"sub": "alice"},
        )


def test_device_and_workload_identities_support_lifecycle_rotation_and_cross_cloud_trust_paths():
    identities = DeviceWorkloadIdentityRegistry()
    trust_graph = TrustFederationGraph()

    device = identities.register_device(
        device_id="device-1",
        subject_id="alice",
        tenant_id="tenant-a",
        credential_posture="managed",
        last_ip_country="US",
    )
    workload = identities.register_workload(
        workload_id="payments-api",
        tenant_id="tenant-a",
        trust_domain="spiffe://aws.example/payments",
        cloud="aws",
        namespace="payments",
        attestor="spire-agent",
    )
    trust_graph.add_domain(
        name="spiffe://aws.example/payments",
        issuers=("https://sts.aws.example",),
        clouds=("aws",),
    )
    trust_graph.add_domain(
        name="trust://hub.example",
        issuers=("https://hub.example",),
        clouds=("aws", "gcp"),
    )
    trust_graph.add_domain(
        name="spiffe://gcp.example/payments",
        issuers=("https://iam.gcp.example",),
        clouds=("gcp",),
    )
    trust_graph.add_edge(
        source_domain="spiffe://aws.example/payments",
        target_domain="trust://hub.example",
        exchange_kind="token-exchange",
        constraints={"audience": "hub"},
    )
    trust_graph.add_edge(
        source_domain="trust://hub.example",
        target_domain="spiffe://gcp.example/payments",
        exchange_kind="federated-workload",
        constraints={"audience": "gcp"},
    )

    rotated = identities.rotate_workload_credential(workload_id="payments-api", tenant_id="tenant-a")
    mapping = trust_graph.map_cross_cloud_workload(
        workload=rotated,
        target_domain="spiffe://gcp.example/payments",
    )
    revoked_device = identities.revoke_device(device_id="device-1", tenant_id="tenant-a")

    assert device.credential_posture == "managed"
    assert rotated.credential_id != workload.credential_id
    assert mapping["path"] == [
        "spiffe://aws.example/payments",
        "trust://hub.example",
        "spiffe://gcp.example/payments",
    ]
    assert mapping["exchange_kinds"] == ["token-exchange", "federated-workload"]
    assert mapping["target_clouds"] == ["gcp"]
    assert revoked_device.revoked


def test_relationship_graph_and_policy_registry_support_rebac_graph_queries_versions_and_decision_api():
    assert PolicyRegistry is CanonicalPolicyRegistry
    assert RelationshipGraph is CanonicalRelationshipGraph

    graph = RelationshipGraph()
    initial = graph.define_relation(resource_type="document", relation="viewer", subject_types=("user",))
    migrated = graph.define_relation(resource_type="document", relation="viewer", subject_types=("group", "user"))
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
    graph.add_tuple(
        resource_type="group",
        resource_id="eng",
        relation="member",
        subject_type="group",
        subject_id="staff",
        tenant_id="tenant-a",
    )
    graph.add_tuple(
        resource_type="group",
        resource_id="staff",
        relation="member",
        subject_type="group",
        subject_id="eng",
        tenant_id="tenant-a",
    )

    policies = PolicyRegistry(relationship_graph=graph)
    policy = policies.create_policy(tenant_id="tenant-a", name="document.read")
    version_1 = policies.publish_version(
        policy_id=policy.policy_id,
        source='allow if relation viewer and context.tenant == "tenant-a" and context.mfa == true',
        promote=True,
    )
    version_2 = policies.publish_version(
        policy_id=policy.policy_id,
        source='allow if relation viewer and context.tenant == "tenant-a" and context.mfa == true and context.device_trusted == true',
        promote=True,
    )
    policies.rollback_policy(policy_id=policy.policy_id, version_id=version_1.version_id)

    allowed = policies.access_decision(
        AccessDecisionRequest(
            tenant_id="tenant-a",
            subject="user:alice",
            action="document.read",
            resource="document:roadmap",
            context={"tenant": "tenant-a", "mfa": True},
            correlation_id="corr-1",
        )
    )
    denied = policies.access_decision(
        AccessDecisionRequest(
            tenant_id="tenant-a",
            subject="user:alice",
            action="document.read",
            resource="document:roadmap",
            context={"tenant": "tenant-a", "mfa": False},
            correlation_id="corr-2",
        )
    )
    no_path = graph.check_access(
        tenant_id="tenant-a",
        subject="user:bob",
        relation="viewer",
        resource="document:roadmap",
    )

    assert initial.version == 1
    assert migrated.version == 2
    assert policies.check_compatibility(left_version_id=version_1.version_id, right_version_id=version_2.version_id)
    assert allowed.allowed
    assert allowed.policy_version_id == version_1.version_id
    assert allowed.idempotency_key == "corr-1:user:alice:document.read:document:roadmap"
    assert any("group:eng#member@user:alice" in step for step in allowed.explanation)
    assert not denied.allowed
    assert denied.reason == "policy context does not satisfy required values"
    assert not no_path.allowed


def test_auth_anomaly_detector_normalizes_redacts_and_explains_detection_outputs():
    detector = AuthAnomalyDetector()
    detector.record_event(
        tenant_id="tenant-a",
        subject_id="alice",
        event_type="login",
        correlation_id="corr-1",
        ip_country="US",
        trusted_device=True,
        outcome="failure",
        details={"access_token": "abc.def.ghi", "ip": "198.51.100.10"},
    )
    detector.record_event(
        tenant_id="tenant-a",
        subject_id="alice",
        event_type="login",
        correlation_id="corr-2",
        ip_country="US",
        trusted_device=False,
        outcome="failure",
        details={"password": "never-log-this", "ip": "198.51.100.11"},
    )
    event, signal = detector.record_event(
        tenant_id="tenant-a",
        subject_id="alice",
        event_type="login",
        correlation_id="corr-3",
        ip_country="DE",
        trusted_device=False,
        outcome="failure",
        details={"refresh_token": "secret", "ip": "203.0.113.44"},
    )

    assert signal is not None
    assert signal.severity == "high"
    assert signal.recommended_action == "manual-review"
    assert "repeated authentication failures" in signal.reasons
    assert "untrusted device telemetry" in signal.reasons
    assert event.details["refresh_token"] == "[REDACTED]"
    assert signal.redacted_details["refresh_token"] == "[REDACTED]"


def test_phase4_delivery_summary_aggregates_advanced_identity_capabilities():
    authenticators = AdvancedAuthenticatorRegistry()
    federation = FederationRegistry()
    non_human = DeviceWorkloadIdentityRegistry()
    graph = RelationshipGraph()
    graph.define_relation(resource_type="document", relation="viewer", subject_types=("user",))
    policies = PolicyRegistry(relationship_graph=graph)
    detector = AuthAnomalyDetector()
    trust_graph = TrustFederationGraph()

    authenticators.enroll_passwordless_credential(subject_id="alice", tenant_id="tenant-a")
    federation.register_provider(
        provider_id="corp-sso",
        tenant_id="tenant-a",
        kind="sso",
        issuer="https://login.example.com",
        discovery_url="https://login.example.com/.well-known/openid-configuration",
        audience="public-uix",
        display_name="Contoso SSO",
    )
    non_human.register_device(
        device_id="device-1",
        subject_id="alice",
        tenant_id="tenant-a",
        credential_posture="managed",
    )
    policy = policies.create_policy(tenant_id="tenant-a", name="document.read")
    policies.publish_version(policy_id=policy.policy_id, source='allow if relation viewer and context.tenant == "tenant-a"')
    detector.record_event(
        tenant_id="tenant-a",
        subject_id="alice",
        event_type="login",
        correlation_id="corr-1",
        ip_country="US",
        trusted_device=True,
        outcome="success",
        details={"session": "ok"},
    )
    trust_graph.add_domain(name="trust://hub.example", issuers=("https://hub.example",), clouds=("aws", "gcp"))

    summary = build_phase4_delivery_summary(
        authenticator_registry=authenticators,
        federation_registry=federation,
        device_workload_registry=non_human,
        relationship_graph=graph,
        policy_registry=policies,
        anomaly_detector=detector,
        trust_graph=trust_graph,
    )

    assert summary["advanced_authentication"]["passwordless_credential_count"] == 1
    assert summary["federation"]["provider_count"] == 1
    assert summary["non_human_identities"]["device_count"] == 1
    assert summary["policy_control_plane"]["policy_count"] == 1
    assert summary["anomaly_detection"]["event_count"] == 1
    assert summary["trust_graph"]["domain_count"] == 1
