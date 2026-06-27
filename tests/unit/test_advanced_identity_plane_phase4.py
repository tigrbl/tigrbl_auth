import pytest

from tigrbl_identity_admin._advanced_identity_plane.authenticators import (
    AdvancedAuthenticatorRegistry as CanonicalAdvancedAuthenticatorRegistry,
)
from tigrbl_identity_admin_auth_anomaly_detector import AuthAnomalyDetector as CanonicalAuthAnomalyDetector
from tigrbl_identity_admin_relationship_graph import RelationshipGraph as CanonicalRelationshipGraph
from tigrbl_identity_admin_trust_federation_graph import (
    TrustFederationGraph as CanonicalTrustFederationGraph,
)
from tigrbl_identity_storage.tables import Federation as CanonicalFederation
from tigrbl_identity_storage.tables import AuthenticationChallenge as CanonicalAuthenticationChallenge
from tigrbl_identity_storage.tables import CredentialMfaFactor, CredentialWebAuthnPasskey
from tigrbl_identity_storage.tables import Policy as CanonicalPolicy
from tigrbl_auth.services.advanced_identity_plane import (
    AccessDecisionRequest,
    AdaptiveContext,
    AdvancedAuthenticatorRegistry,
    AuthAnomalyDetector,
    DeviceWorkloadIdentityRegistry,
    Federation,
    Policy,
    RelationshipGraph,
    TrustFederationGraph,
    build_phase4_delivery_summary,
)


def test_advanced_authenticator_registry_supports_passwordless_webauthn_mfa_and_replay_safety():
    assert AdvancedAuthenticatorRegistry is CanonicalAdvancedAuthenticatorRegistry

    registry = AdvancedAuthenticatorRegistry()
    assert registry.challenge_table is CanonicalAuthenticationChallenge
    assert registry.mfa_factor_table is CredentialMfaFactor
    assert registry.webauthn_passkey_table is CredentialWebAuthnPasskey
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


def test_deprecated_advanced_authenticator_registry_reexports_admin_surface():
    with pytest.warns(DeprecationWarning):
        from tigrbl_identity_admin_advanced_authenticator_registry import (
            AdvancedAuthenticatorRegistry as DeprecatedAdvancedAuthenticatorRegistry,
        )

    assert DeprecatedAdvancedAuthenticatorRegistry is AdvancedAuthenticatorRegistry


def test_federation_surface_exports_storage_table_registry() -> None:
    assert Federation is CanonicalFederation


def test_device_and_workload_identities_support_lifecycle_rotation_and_cross_cloud_trust_paths():
    assert TrustFederationGraph is CanonicalTrustFederationGraph

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


def test_relationship_graph_and_policy_surface_use_table_owned_policy_state():
    assert Policy is CanonicalPolicy
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

    no_path = graph.check_access(
        tenant_id="tenant-a",
        subject="user:bob",
        relation="viewer",
        resource="document:roadmap",
    )

    assert initial.version == 1
    assert migrated.version == 2
    assert not no_path.allowed


def test_auth_anomaly_detector_normalizes_redacts_and_explains_detection_outputs():
    assert AuthAnomalyDetector is CanonicalAuthAnomalyDetector

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
    federation = Federation
    non_human = DeviceWorkloadIdentityRegistry()
    graph = RelationshipGraph()
    graph.define_relation(resource_type="document", relation="viewer", subject_types=("user",))
    policies = Policy
    detector = AuthAnomalyDetector()
    trust_graph = TrustFederationGraph()

    authenticators.enroll_passwordless_credential(subject_id="alice", tenant_id="tenant-a")
    non_human.register_device(
        device_id="device-1",
        subject_id="alice",
        tenant_id="tenant-a",
        credential_posture="managed",
    )
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
    assert summary["federation"]["provider_count"] == 0
    assert summary["non_human_identities"]["device_count"] == 1
    assert summary["policy_control_plane"]["policy_count"] == 0
    assert summary["anomaly_detection"]["event_count"] == 1
    assert summary["trust_graph"]["domain_count"] == 1
