from __future__ import annotations

import json
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient

from tigrbl_auth.api.app import build_app
from tigrbl_auth.api.rpc.registry import RpcRequestContext, invoke_rpc_method_async, list_rpc_methods
from tigrbl_auth.cli.artifacts import deployment_from_options
from tigrbl_auth.services._operator_store import OperationContext
from tigrbl_auth.services.operator_service import create_resource

ROOT_ISSUER = "https://id.example.com"
TENANT_A = "tenant-a"
TENANT_B = "tenant-b"


def _deployment():
    return deployment_from_options(profile="baseline-development", issuer=ROOT_ISSUER)


def _context(tmp_path: Path) -> RpcRequestContext:
    return RpcRequestContext(repo_root=tmp_path, profile="production", deployment=_deployment())


def _seed_tenants(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TIGRBL_AUTH_OPERATOR_STATE_DIR", str(tmp_path / ".operator-state"))
    monkeypatch.chdir(tmp_path)
    tenant_ctx = OperationContext(repo_root=tmp_path, command="tenant.create", resource="tenant", actor="test")
    create_resource(tenant_ctx, record_id=TENANT_A, patch={"name": "Tenant A"}, if_exists="error")
    create_resource(tenant_ctx, record_id=TENANT_B, patch={"name": "Tenant B"}, if_exists="error")


@pytest.mark.asyncio
async def test_tenant_jwks_key_admin_rpc_methods_are_registered() -> None:
    methods = {item.name for item in list_rpc_methods()}

    assert {"tenant.keys.seed", "tenant.keys.create", "tenant.keys.update", "tenant.keys.delete"} <= methods


@pytest.mark.asyncio
async def test_tenant_jwks_key_admin_rpc_methods_are_served_over_http(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _seed_tenants(tmp_path, monkeypatch)
    monkeypatch.setenv("TIGRBL_AUTH_ADMIN_API_KEY", "test-admin-key")

    async with AsyncClient(transport=ASGITransport(app=build_app(deployment=_deployment())), base_url=ROOT_ISSUER) as client:
        response = await client.post(
            "/rpc",
            headers={"X-API-Key": "test-admin-key"},
            json={
                "jsonrpc": "2.0",
                "id": "seed-a",
                "method": "tenant.keys.seed",
                "params": {"tenant": TENANT_A},
            },
        )

    assert response.status_code == 200
    payload = response.json()
    assert payload["id"] == "seed-a"
    assert payload["result"]["status"] == "created"
    assert payload["result"]["key"]["kid"] == f"{TENANT_A}-jwks-active"


@pytest.mark.asyncio
async def test_tenant_jwks_key_seed_is_idempotent_and_publishable(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _seed_tenants(tmp_path, monkeypatch)
    context = _context(tmp_path)

    first = await invoke_rpc_method_async("tenant.keys.seed", {"tenant": TENANT_A}, context=context)
    second = await invoke_rpc_method_async("tenant.keys.seed", {"tenant": TENANT_A}, context=context)

    assert first["status"] == "created"
    assert second["status"] == "exists"
    assert first["key"]["kid"] == second["key"]["kid"]
    assert first["jwks"]["keys"][0]["kid"] == first["key"]["kid"]


@pytest.mark.asyncio
async def test_tenant_jwks_key_crud_updates_public_jwks_and_preserves_tenant_isolation(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _seed_tenants(tmp_path, monkeypatch)
    context = _context(tmp_path)

    await invoke_rpc_method_async(
        "tenant.keys.create",
        {"tenant": TENANT_A, "kid": "kid-a-active", "status": "active", "x": "pub-a", "publish": True},
        context=context,
    )
    await invoke_rpc_method_async(
        "tenant.keys.create",
        {"tenant": TENANT_B, "kid": "kid-b-active", "status": "active", "x": "pub-b", "publish": True},
        context=context,
    )

    async with AsyncClient(transport=ASGITransport(app=build_app(deployment=_deployment())), base_url=ROOT_ISSUER) as client:
        tenant_a_jwks = await client.get(f"/tenants/{TENANT_A}/.well-known/jwks.json")
    serialized = json.dumps(tenant_a_jwks.json(), sort_keys=True)
    assert tenant_a_jwks.status_code == 200
    assert "kid-a-active" in serialized
    assert "kid-b-active" not in serialized
    assert "pub-b" not in serialized

    retired = await invoke_rpc_method_async(
        "tenant.keys.update",
        {"tenant": TENANT_A, "kid": "kid-a-active", "status": "retired", "publish": False},
        context=context,
    )
    assert retired["key"]["metadata"]["status"] == "retired"
    assert retired["jwks"]["keys"] == []

    deleted = await invoke_rpc_method_async("tenant.keys.delete", {"tenant": TENANT_A, "kid": "kid-a-active"}, context=context)
    assert deleted["status"] == "deleted"
    listed = await invoke_rpc_method_async("keys.list", {"tenant": TENANT_A}, context=context)
    assert listed["keys"] == []


@pytest.mark.asyncio
async def test_tenant_jwks_key_mutations_reject_cross_tenant_updates(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _seed_tenants(tmp_path, monkeypatch)
    context = _context(tmp_path)
    await invoke_rpc_method_async("tenant.keys.create", {"tenant": TENANT_A, "kid": "kid-a", "x": "pub-a"}, context=context)

    with pytest.raises(Exception, match="was not found"):
        await invoke_rpc_method_async("tenant.keys.update", {"tenant": TENANT_B, "kid": "kid-a", "status": "retired"}, context=context)
