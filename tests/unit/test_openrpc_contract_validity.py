from __future__ import annotations

import json
from types import SimpleNamespace

import pytest
from httpx import ASGITransport, AsyncClient

from tigrbl_auth.api.app import build_app
from tigrbl_auth.cli.artifacts import build_openrpc_contract, deployment_from_options
from tigrbl_auth.config.deployment import resolve_deployment


PROFILES = ("baseline", "production", "hardening", "fapi2-security", "peer-claim")


def _assert_openrpc_contract_valid(contract: dict, deployment: object) -> None:
    json.dumps(contract)

    assert str(contract.get("openrpc", "")).startswith("1.")
    assert contract.get("info", {}).get("title")
    assert contract.get("info", {}).get("version")
    assert contract.get("servers") == []

    xmeta = contract.get("x-tigrbl-auth", {})
    assert xmeta.get("profile") == getattr(deployment, "profile")
    assert xmeta.get("generation_mode") == "rest-only-no-rpc"

    methods = contract.get("methods", [])
    assert methods == []


def _assert_runtime_openrpc_payload_valid(payload: dict) -> None:
    json.dumps(payload)

    assert str(payload.get("openrpc", "")).startswith("1.")
    assert payload.get("info", {}).get("title")
    assert payload.get("info", {}).get("version")
    assert payload.get("servers") == []
    assert isinstance(payload.get("methods"), list)
    assert len(payload["methods"]) == len({item["name"] for item in payload["methods"]})


def _settings(tmp_path) -> SimpleNamespace:
    return SimpleNamespace(admin_api_key="test-admin-key", admin_api_key_dir=str(tmp_path))


@pytest.mark.parametrize("profile", PROFILES)
def test_openrpc_builder_remains_valid_when_endpoint_is_hidden(profile: str) -> None:
    deployment = deployment_from_options(profile=profile)
    contract = build_openrpc_contract(deployment, version="0.0.0-test")
    _assert_openrpc_contract_valid(contract, deployment)


@pytest.mark.parametrize("profile", PROFILES)
def test_openrpc_builder_remains_valid_when_endpoint_is_exposed(profile: str) -> None:
    deployment = deployment_from_options(profile=profile, plugin_mode="mixed")
    contract = build_openrpc_contract(deployment, version="0.0.0-test")
    _assert_openrpc_contract_valid(contract, deployment)


@pytest.mark.asyncio
async def test_hidden_openrpc_endpoint_still_has_valid_builder_output(tmp_path) -> None:
    deployment = resolve_deployment()
    app = build_app(_settings(tmp_path), deployment=deployment)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/openrpc.json")

    assert response.status_code == 404

    contract = build_openrpc_contract(deployment, version="0.0.0-test")
    _assert_openrpc_contract_valid(contract, deployment)
    assert contract["methods"] == []


@pytest.mark.asyncio
async def test_mixed_runtime_openrpc_endpoint_is_absent(tmp_path) -> None:
    deployment = resolve_deployment(plugin_mode="mixed")
    app = build_app(_settings(tmp_path), deployment=deployment)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/openrpc.json")

    assert response.status_code == 404
