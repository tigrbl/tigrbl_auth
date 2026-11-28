from tba_durability_identity_administration_trust_federation_graph import (
    TrustFederationGraph as CanonicalTrustFederationGraph,
    TrustFederationGraphEdgeRuntimeSpec,
    TrustFederationGraphNodeRuntimeSpec,
    TrustFederationGraphRuntimeSpec,
)
from tba_storage_core.tables import (
    TrustFederationGraph as TrustFederationGraphTable,
    TrustFederationGraphEdge,
    TrustFederationGraphNode,
)
from tba_auth.services.advanced_identity_plane import (
    DeviceWorkloadIdentityRegistry,
    TrustFederationGraph,
)


def test_device_and_workload_identities_support_lifecycle_rotation_and_cross_cloud_trust_paths():
    assert TrustFederationGraph is CanonicalTrustFederationGraph
    assert TrustFederationGraphRuntimeSpec.model is TrustFederationGraphTable
    assert TrustFederationGraphNodeRuntimeSpec.model is TrustFederationGraphNode
    assert TrustFederationGraphEdgeRuntimeSpec.model is TrustFederationGraphEdge

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

    rotated = identities.rotate_workload_credential(
        workload_id="payments-api", tenant_id="tenant-a"
    )
    mapping = trust_graph.map_cross_cloud_workload(
        workload=rotated,
        target_domain="spiffe://gcp.example/payments",
    )
    revoked_device = identities.revoke_device(
        device_id="device-1", tenant_id="tenant-a"
    )

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
