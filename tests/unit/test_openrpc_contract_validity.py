from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest
from httpx import ASGITransport, AsyncClient

from tigrbl_auth.api.app import build_app
from tigrbl_auth.api.rpc import iter_active_rpc_methods
from tigrbl_auth.cli.artifacts import build_openrpc_contract, deployment_from_options
from tigrbl_auth.config.deployment import resolve_deployment


PROFILES = ("baseline", "production", "hardening", "fapi2-security", "peer-claim")


def _assert_openrpc_contract_valid(contract: dict, deployment: object) -> None:
    json.dumps(contract)

    assert str(contract.get("openrpc", "")).startswith("1.")
    assert contract.get("info", {}).get("title")
    assert contract.get("info", {}).get("version")
    assert contract.get("servers") == [{"name": "admin-rpc", "url": f"{deployment.issuer}/rpc"}]

    xmeta = contract.get("x-tigrbl-auth", {})
    assert xmeta.get("profile") == getattr(deployment, "profile")
    assert xmeta.get("generation_mode") == "implementation-backed-rpc-registry"

    methods = contract.get("methods", [])
    assert len(methods) == len({item["name"] for item in methods})

    expected = {item.name for item in iter_active_rpc_methods(deployment)}
    actual = {item["name"] for item in methods}
    assert actual == expected

    if deployment.surface_enabled("admin-rpc"):
        components = contract.get("components", {})
        assert components.get("schemas")
        security_schemes = components.get("securitySchemes", {})
        assert security_schemes["AdminApiKeyHeader"]["name"] == "X-API-Key"
        assert security_schemes["AdminBearer"]["scheme"] == "bearer"
        assert methods
        for method in methods:
            assert method.get("security")
            assert method["paramStructure"] == "by-name"
            assert isinstance(method.get("params"), list)
            assert method["result"]["schema"]["$ref"].startswith("#/components/schemas/")
            owner_module = method["x-tigrbl-auth"]["owner_module"]
            assert owner_module.startswith("tigrbl_auth/api/rpc/methods/")
            assert Path(owner_module).exists()
    else:
        assert methods == []


def _assert_runtime_openrpc_payload_valid(payload: dict) -> None:
    json.dumps(payload)

    assert str(payload.get("openrpc", "")).startswith("1.")
    assert payload.get("info", {}).get("title")
    assert payload.get("info", {}).get("version")
    assert payload.get("servers")
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

    assert response.status_code == 200
    payload = response.json()
    _assert_runtime_openrpc_payload_valid(payload)
    assert payload["methods"] == []

    contract = build_openrpc_contract(deployment, version="0.0.0-test")
    _assert_openrpc_contract_valid(contract, deployment)


@pytest.mark.asyncio
async def test_exposed_openrpc_payload_remains_valid(tmp_path) -> None:
    deployment = resolve_deployment(plugin_mode="mixed")
    app = build_app(_settings(tmp_path), deployment=deployment)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/openrpc.json")

    assert response.status_code == 200
    payload = response.json()
    _assert_runtime_openrpc_payload_valid(payload)
    assert payload["methods"]
