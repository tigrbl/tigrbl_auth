from __future__ import annotations

from typing import Any

from .authorization import RelationshipGraph
from .authenticators import AdvancedAuthenticatorRegistry
from .identities import DeviceWorkloadIdentityRegistry
from .telemetry import AuthAnomalyDetector
from .trust import TrustFederationGraph


def _federation_summary(federation: Any) -> dict[str, Any]:
    summary = getattr(federation, "summary", None)
    if callable(summary):
        return dict(summary())
    return {
        "provider_count": 0,
        "active_provider_count": 0,
        "kinds": [],
        "session_count": 0,
    }


def _policy_summary(policy: Any) -> dict[str, Any]:
    definitions = getattr(policy, "definitions", {})
    versions = getattr(policy, "versions", {})
    if callable(definitions):
        definitions = definitions()
    if callable(versions):
        versions = versions()
    versions_values = tuple(getattr(versions, "values", lambda: ())())
    return {
        "policy_count": len(definitions) if hasattr(definitions, "__len__") else 0,
        "policy_version_count": len(versions_values),
        "active_policy_count": len(
            {
                version.policy_id
                for version in versions_values
                if getattr(version, "promoted", False)
            }
        ),
    }


def build_advanced_identity_graph_auth_delivery_summary(
    *,
    authenticator_registry: AdvancedAuthenticatorRegistry,
    federation_registry: Any,
    device_workload_registry: DeviceWorkloadIdentityRegistry,
    relationship_graph: RelationshipGraph,
    policy_registry: Any,
    anomaly_detector: AuthAnomalyDetector,
    trust_graph: TrustFederationGraph,
) -> dict[str, Any]:
    return {
        "advanced_authentication": authenticator_registry.summary(),
        "federation": _federation_summary(federation_registry),
        "non_human_identities": device_workload_registry.summary(),
        "relationship_graph": {
            "definition_count": len(relationship_graph.definitions),
            "tuple_count": len(relationship_graph.tuples),
        },
        "policy_control_plane": _policy_summary(policy_registry),
        "anomaly_detection": anomaly_detector.summary(),
        "trust_graph": {
            "domain_count": len(trust_graph.domains),
            "edge_count": len(trust_graph.edges),
        },
    }


build_phase4_delivery_summary = build_advanced_identity_graph_auth_delivery_summary
