from tba_auth.services.advanced_identity_plane import (
    AdvancedAuthenticatorRegistry,
    AuthAnomalyDetector,
    DeviceWorkloadIdentityRegistry,
    Federation,
    Policy,
    RelationshipGraph,
    TrustFederationGraph,
    build_phase4_delivery_summary,
)


def test_phase4_delivery_summary_aggregates_advanced_identity_capabilities():
    authenticators = AdvancedAuthenticatorRegistry()
    federation = Federation
    non_human = DeviceWorkloadIdentityRegistry()
    graph = RelationshipGraph()
    graph.define_relation(
        resource_type="document", relation="viewer", subject_types=("user",)
    )
    policies = Policy
    detector = AuthAnomalyDetector()
    trust_graph = TrustFederationGraph()

    authenticators.enroll_passwordless_credential(
        subject_id="alice", tenant_id="tenant-a"
    )
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
    trust_graph.add_domain(
        name="trust://hub.example",
        issuers=("https://hub.example",),
        clouds=("aws", "gcp"),
    )

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
