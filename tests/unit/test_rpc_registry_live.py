from __future__ import annotations

import tigrbl_auth
from tigrbl_identity_cli.cli.artifacts import (
    build_openrpc_contract,
    deployment_from_options,
)


def test_facade_does_not_export_removed_api_namespace() -> None:
    assert "api" not in tigrbl_auth.__all__
    assert "api" not in dir(tigrbl_auth)


def test_openrpc_contract_is_empty_compatibility_artifact() -> None:
    deployment = deployment_from_options(profile="production", plugin_mode="mixed")
    contract = build_openrpc_contract(deployment, version="0.0.0-test")
    assert contract["methods"] == []
    assert contract["x-tigrbl-auth"]["generation_mode"] == "rest-only-no-rpc"
