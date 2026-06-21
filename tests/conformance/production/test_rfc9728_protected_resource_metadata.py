from __future__ import annotations

import json
from pathlib import Path

from tigrbl_auth.cli.artifacts import build_openapi_contract, deployment_from_options
from tigrbl_auth.standards.oauth2.resource_verifier_contract import build_protected_resource_verifier_contract
from tigrbl_auth_protocol_oauth.standards.protected_resource_metadata import build_protected_resource_metadata


ROOT = Path(__file__).resolve().parents[3]


def test_rfc9728_protected_resource_metadata_surface_is_published() -> None:
    deployment = deployment_from_options(profile="production")
    openapi = build_openapi_contract(deployment, version="0.0.0-test")
    metadata = json.loads((ROOT / "specs" / "discovery" / "profiles" / "production" / "oauth-protected-resource.json").read_text(encoding="utf-8"))

    assert "/.well-known/oauth-protected-resource" in deployment.active_routes
    assert "/.well-known/oauth-protected-resource" in openapi["paths"]
    assert metadata["resource"]
    assert metadata["authorization_servers"]


def test_rfc9728_metadata_is_derived_from_verifier_contract() -> None:
    deployment = deployment_from_options(profile="fapi2-security")
    contract = build_protected_resource_verifier_contract(deployment)
    metadata = build_protected_resource_metadata(deployment)

    assert metadata["authorization_servers"] == list(contract.accepted_issuers)
    assert metadata["resource"] == contract.resource
    assert metadata["proof_modes_supported"] == list(contract.sender_constraint_modes)
    assert metadata["proof_binding_required"] == contract.sender_constraint_required
    assert metadata["introspection_endpoint_auth_methods_supported"] == list(contract.introspection_auth_methods)
