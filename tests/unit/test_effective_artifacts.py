from __future__ import annotations

from pathlib import Path

from tigrbl_auth.cli.artifacts import (
    build_effective_claims_manifest,
    build_openapi_contract,
    deployment_from_options,
)
from tigrbl_auth.config.deployment import ROUTE_REGISTRY


def test_effective_claims_do_not_exceed_profile_boundary() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    deployment = deployment_from_options(profile="baseline")
    manifest = build_effective_claims_manifest(repo_root, deployment)
    targets = {claim["target"] for claim in manifest["claim_set"]["claims"]}
    assert "OpenRPC 1.4.x admin/control-plane contract" not in targets
    assert "RFC 9728" not in targets


def test_openapi_contract_matches_resolved_public_routes() -> None:
    deployment = deployment_from_options(profile="baseline")
    contract = build_openapi_contract(deployment, version="test")
    assert set(contract["paths"]) == {
        path
        for path in deployment.active_contract_routes
        if ROUTE_REGISTRY[path].get("surface_set") == "public-rest"
    }
