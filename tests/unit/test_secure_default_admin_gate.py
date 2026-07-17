from __future__ import annotations

import importlib
from types import SimpleNamespace

import pytest
from httpx import ASGITransport, AsyncClient

from tigrbl_auth_backend_app_core import build_app
from tigrbl_auth.config.deployment import resolve_deployment


def _settings(tmp_path, key: str = "test-admin-key") -> SimpleNamespace:
    return SimpleNamespace(admin_api_key=key, admin_api_key_dir=str(tmp_path))


def test_admin_gate_canonical_package_owns_public_surface():
    canonical = importlib.import_module("tigrbl_auth_router_admin_gate")
    facade = importlib.import_module("tigrbl_auth.security.admin_gate")

    assert facade is canonical
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module("tigrbl_identity_server.security.admin_gate")


@pytest.mark.asyncio
async def test_default_runtime_exposes_public_only_surface(tmp_path):
    deployment = resolve_deployment()
    app = build_app(_settings(tmp_path), deployment=deployment)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        discovery = await client.get("/.well-known/openid-configuration")
        tenant = await client.get("/tenant")
        rpc = await client.post(
            "/rpc",
            json={"jsonrpc": "2.0", "method": "CredentialApiKey.create", "params": {}, "id": 1},
        )
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
    deployment = resolve_deployment(product_surface="developer-app")
    app = build_app(_settings(tmp_path), deployment=deployment)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        missing = await client.get("/client")
        invalid = await client.get("/client", headers={"X-API-Key": "wrong"})
        rpc = await client.post(
            "/rpc",
            json={"jsonrpc": "2.0", "method": "CredentialApiKey.create", "params": {}, "id": 1},
            headers={"Authorization": "Bearer test-admin-key"},
        )

    assert missing.status_code == 401
    assert missing.json()["error"] == "missing_admin_api_key"
    assert invalid.status_code == 403
    assert invalid.json()["error"] == "invalid_admin_api_key"
    assert rpc.status_code == 404


@pytest.mark.asyncio
async def test_admin_enabled_runtime_defers_openapi_payload_to_upstream_app(tmp_path):
    deployment = resolve_deployment(plugin_mode="mixed")
    wrapped = build_app(_settings(tmp_path), deployment=deployment)
    inner = wrapped.app
    async with AsyncClient(transport=ASGITransport(app=wrapped), base_url="http://test") as wrapped_client:
        wrapped_openapi = (await wrapped_client.get("/openapi.json")).json()
    async with AsyncClient(transport=ASGITransport(app=inner), base_url="http://test") as inner_client:
        inner_openapi = (await inner_client.get("/openapi.json")).json()

    assert wrapped_openapi == inner_openapi


@pytest.mark.asyncio
async def test_admin_enabled_runtime_openapi_declares_tigrbl_security_dependencies(tmp_path):
    deployment = resolve_deployment(plugin_mode="mixed")
    app = build_app(_settings(tmp_path), deployment=deployment)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        openapi = (await client.get("/openapi.json")).json()

    security_schemes = openapi["components"]["securitySchemes"]
    assert security_schemes["AdminApiKeyHeader"] == {"type": "apiKey", "in": "header", "name": "X-API-Key"}
    assert security_schemes["AdminBearer"] == {"type": "http", "scheme": "bearer"}
    assert "/tenant" in openapi["paths"]
    assert "security" not in openapi["paths"]["/.well-known/openid-configuration"]["get"]
