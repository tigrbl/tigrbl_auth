from __future__ import annotations

from typing import Any

from .authenticators import AdvancedAuthenticatorRegistry
from .authorization import PolicyRegistry, RelationshipGraph
from .federation import FederationRegistry
from .identities import DeviceWorkloadIdentityRegistry
from .telemetry import AuthAnomalyDetector
from .trust import TrustFederationGraph


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
