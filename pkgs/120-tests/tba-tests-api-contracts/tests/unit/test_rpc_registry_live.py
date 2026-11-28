from __future__ import annotations

import tba_auth
from tba_cli_identity.cli.artifacts import (
    build_openrpc_contract,
    deployment_from_options,
)


def test_facade_does_not_export_removed_api_namespace() -> None:
    assert "api" not in tba_auth.__all__
    assert "api" not in dir(tba_auth)


def test_openrpc_contract_is_empty_compatibility_artifact() -> None:
    deployment = deployment_from_options(profile="production", plugin_mode="mixed")
    contract = build_openrpc_contract(deployment, version="0.0.0-test")
    assert contract["methods"] == []
    assert contract["x-tba-auth"]["generation_mode"] == "rest-only-no-rpc"
