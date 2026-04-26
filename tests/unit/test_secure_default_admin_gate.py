from __future__ import annotations

from types import SimpleNamespace

import pytest
from httpx import ASGITransport, AsyncClient

from tigrbl_auth.api.app import build_app
from tigrbl_auth.cli.artifacts import build_openrpc_contract, deployment_from_options
from tigrbl_auth.config.deployment import resolve_deployment


def _settings(tmp_path, key: str = "test-admin-key") -> SimpleNamespace:
    return SimpleNamespace(admin_api_key=key, admin_api_key_dir=str(tmp_path))


@pytest.mark.asyncio
async def test_default_runtime_exposes_public_only_surface(tmp_path):
    deployment = resolve_deployment()
    app = build_app(_settings(tmp_path), deployment=deployment)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        discovery = await client.get("/.well-known/openid-configuration")
        tenant = await client.get("/tenant")
        rpc = await client.post("/rpc", json={"jsonrpc": "2.0", "method": "ApiKey.create", "params": {}, "id": 1})
        diagnostics = await client.get("/system/healthz")
        openapi = (await client.get("/openapi.json")).json()

    assert deployment.plugin_mode == "public-only"
    assert discovery.status_code == 200
    assert tenant.status_code == 404
    assert rpc.status_code == 404
    assert diagnostics.status_code == 404
    assert not any(path.startswith("/system") for path in openapi["paths"])


@pytest.mark.asyncio
async def test_admin_enabled_runtime_requires_local_admin_key(tmp_path):
    deployment = resolve_deployment(plugin_mode="mixed")
    app = build_app(_settings(tmp_path), deployment=deployment)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        missing = await client.get("/tenant")
        invalid = await client.get("/tenant", headers={"X-API-Key": "wrong"})
        valid = await client.post(
            "/rpc",
            json={"jsonrpc": "2.0", "method": "ApiKey.create", "params": {}, "id": 1},
            headers={"Authorization": "Bearer test-admin-key"},
        )

    assert missing.status_code == 401
    assert missing.json()["error"] == "missing_admin_api_key"
    assert invalid.status_code == 403
    assert invalid.json()["error"] == "invalid_admin_api_key"
    assert valid.status_code not in {401, 403}


@pytest.mark.asyncio
async def test_admin_enabled_runtime_marks_protected_contract_surfaces(tmp_path):
    deployment = resolve_deployment(plugin_mode="mixed")
    app = build_app(_settings(tmp_path), deployment=deployment)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        openapi = (await client.get("/openapi.json")).json()
        openrpc = (await client.get("/openrpc.json")).json()

    assert openapi["components"]["securitySchemes"]["AdminApiKeyHeader"]["name"] == "X-API-Key"
    assert openapi["paths"]["/tenant"]["get"]["security"]
    assert "security" not in openapi["paths"]["/.well-known/openid-configuration"]["get"]
    assert openrpc["components"]["securitySchemes"]["AdminBearer"]["scheme"] == "bearer"
    assert all(method.get("security") for method in openrpc["methods"])


def test_openrpc_artifact_marks_admin_methods_with_security():
    deployment = deployment_from_options(profile="baseline", plugin_mode="mixed")
    contract = build_openrpc_contract(deployment, version="0.0.0-test")
    assert contract["components"]["securitySchemes"]["AdminApiKeyHeader"]["in"] == "header"
    assert all(method.get("security") for method in contract["methods"])
