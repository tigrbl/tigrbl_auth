from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest
from httpx import ASGITransport, AsyncClient

from tigrbl_auth.api.app import build_app
from tigrbl_auth.cli.artifacts import build_openapi_contract, deployment_from_options, write_discovery_artifacts
from tigrbl_auth.services._operator_store import OperationContext
from tigrbl_auth.services.operator_service import create_resource, generate_key_record, publish_jwks_document
from tigrbl_auth.services.tenant_discovery import (
    TENANT_JWKS_PATH,
    TENANT_OPENID_CONFIGURATION_PATH,
    require_tenant_issuer,
    tenant_issuer,
)

ROOT_ISSUER = "https://id.example.com"
TENANT_A = "tenant-a"
TENANT_B = "tenant-b"


def _settings(tmp_path: Path) -> SimpleNamespace:
    return SimpleNamespace(admin_api_key="test-admin-key", admin_api_key_dir=str(tmp_path))


def _deployment():
    return deployment_from_options(profile="production", issuer=ROOT_ISSUER)


def _context(tmp_path: Path, resource: str, command: str, *, tenant: str | None = None) -> OperationContext:
    return OperationContext(repo_root=tmp_path, command=command, resource=resource, actor="feature", profile="production", tenant=tenant)


def _seed_operator_state(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TIGRBL_AUTH_OPERATOR_STATE_DIR", str(tmp_path / ".operator-state"))
    monkeypatch.chdir(tmp_path)

    tenant_ctx = _context(tmp_path, "tenant", "tenant.create")
    create_resource(tenant_ctx, record_id=TENANT_A, patch={"name": "Tenant A"}, if_exists="error")
    create_resource(tenant_ctx, record_id=TENANT_B, patch={"name": "Tenant B"}, if_exists="error")
    create_resource(tenant_ctx, record_id="tenant-disabled", patch={"name": "Disabled", "enabled": False}, if_exists="error")

    generate_key_record(_context(tmp_path, "keys", "keys.generate", tenant=TENANT_A), patch={"kid": "kid-a-active", "status": "active", "x": "a-active"})
    generate_key_record(_context(tmp_path, "keys", "keys.generate", tenant=TENANT_A), patch={"kid": "kid-a-next", "status": "next", "x": "a-next"})
    generate_key_record(_context(tmp_path, "keys", "keys.generate", tenant=TENANT_A), patch={"kid": "kid-a-retired", "status": "retired", "x": "a-retired"})
    generate_key_record(_context(tmp_path, "keys", "keys.generate", tenant=TENANT_B), patch={"kid": "kid-b-active", "status": "active", "x": "b-active"})


async def _client(tmp_path: Path) -> AsyncClient:
    app = build_app(_settings(tmp_path), deployment=_deployment())
    return AsyncClient(transport=ASGITransport(app=app), base_url=ROOT_ISSUER)


@pytest.mark.asyncio
async def test_tenant_scoped_issuer_boundary_contract(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _seed_operator_state(tmp_path, monkeypatch)
    async with await _client(tmp_path) as client:
        response = await client.get(f"/tenants/{TENANT_A}/.well-known/openid-configuration")
    assert response.status_code == 200
    assert response.json()["issuer"] == tenant_issuer(ROOT_ISSUER, TENANT_A)


@pytest.mark.asyncio
async def test_tenant_openid_configuration_route_contract(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _seed_operator_state(tmp_path, monkeypatch)
    async with await _client(tmp_path) as client:
        response = await client.get(f"/tenants/{TENANT_A}/.well-known/openid-configuration")
    assert response.status_code == 200
    assert response.json()["issuer"].endswith(f"/tenants/{TENANT_A}")


@pytest.mark.asyncio
async def test_tenant_jwks_route_contract(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _seed_operator_state(tmp_path, monkeypatch)
    async with await _client(tmp_path) as client:
        response = await client.get(f"/tenants/{TENANT_A}/.well-known/jwks.json")
    assert response.status_code == 200
    assert response.json()["keys"]


@pytest.mark.asyncio
async def test_tenant_discovery_jwks_uri_contract(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _seed_operator_state(tmp_path, monkeypatch)
    async with await _client(tmp_path) as client:
        response = await client.get(f"/tenants/{TENANT_A}/.well-known/openid-configuration")
    assert response.json()["jwks_uri"] == f"{ROOT_ISSUER}/tenants/{TENANT_A}/.well-known/jwks.json"


@pytest.mark.asyncio
async def test_tenant_jwks_key_filtering_contract(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _seed_operator_state(tmp_path, monkeypatch)
    async with await _client(tmp_path) as client:
        response = await client.get(f"/tenants/{TENANT_A}/.well-known/jwks.json")
    kids = {key["kid"] for key in response.json()["keys"]}
    assert "kid-a-active" in kids
    assert "kid-b-active" not in kids


@pytest.mark.asyncio
async def test_tenant_jwks_rotation_visibility_contract(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _seed_operator_state(tmp_path, monkeypatch)
    async with await _client(tmp_path) as client:
        response = await client.get(f"/tenants/{TENANT_A}/.well-known/jwks.json")
    kids = {key["kid"] for key in response.json()["keys"]}
    assert {"kid-a-active", "kid-a-next"} <= kids
    assert "kid-a-retired" not in kids


@pytest.mark.asyncio
async def test_tenant_public_discovery_disabled_policy_contract(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _seed_operator_state(tmp_path, monkeypatch)
    async with await _client(tmp_path) as client:
        missing = await client.get("/tenants/missing/.well-known/openid-configuration")
        disabled = await client.get("/tenants/tenant-disabled/.well-known/jwks.json")
    assert missing.status_code == 404
    assert disabled.status_code == 404


@pytest.mark.asyncio
async def test_operator_tenant_jwks_runtime_parity_contract(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _seed_operator_state(tmp_path, monkeypatch)
    operator = publish_jwks_document(_context(tmp_path, "keys", "keys.publish-jwks", tenant=TENANT_A))
    operator_payload = json.loads((tmp_path / operator.path).read_text(encoding="utf-8"))
    async with await _client(tmp_path) as client:
        runtime = await client.get(f"/tenants/{TENANT_A}/.well-known/jwks.json")
    assert runtime.json() == operator_payload


def test_openapi_tenant_discovery_routes_contract() -> None:
    contract = build_openapi_contract(_deployment(), version="0.0.0-test")
    assert TENANT_OPENID_CONFIGURATION_PATH in contract["paths"]
    assert TENANT_JWKS_PATH in contract["paths"]
    assert contract["paths"][TENANT_OPENID_CONFIGURATION_PATH]["get"]["parameters"][0]["name"] == "tenant_slug"
    assert contract["paths"][TENANT_JWKS_PATH]["get"]["parameters"][0]["name"] == "tenant_slug"


def test_discovery_snapshot_tenant_profile_artifacts_contract(tmp_path: Path) -> None:
    written = write_discovery_artifacts(tmp_path, _deployment(), profile_label="production")
    assert "tenants/tenant-a/openid-configuration.json" in written
    payload = json.loads(written["tenants/tenant-a/openid-configuration.json"].read_text(encoding="utf-8"))
    assert payload["issuer"] == f"{ROOT_ISSUER}/tenants/tenant-a"
    assert payload["jwks_uri"] == f"{ROOT_ISSUER}/tenants/tenant-a/.well-known/jwks.json"


def test_tenant_issuer_token_validation_contract() -> None:
    require_tenant_issuer({"iss": f"{ROOT_ISSUER}/tenants/{TENANT_A}"}, root_issuer=ROOT_ISSUER, tenant_slug=TENANT_A)
    with pytest.raises(ValueError, match="tenant token issuer mismatch"):
        require_tenant_issuer({"iss": ROOT_ISSUER}, root_issuer=ROOT_ISSUER, tenant_slug=TENANT_A)


@pytest.mark.asyncio
async def test_tenant_jwks_cross_tenant_leakage_guard_contract(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _seed_operator_state(tmp_path, monkeypatch)
    async with await _client(tmp_path) as client:
        discovery = await client.get(f"/tenants/{TENANT_A}/.well-known/openid-configuration")
        jwks = await client.get(f"/tenants/{TENANT_A}/.well-known/jwks.json")
    combined = json.dumps({"discovery": discovery.json(), "jwks": jwks.json()}, sort_keys=True)
    assert "kid-b-active" not in combined
    assert f"/tenants/{TENANT_B}" not in combined


@pytest.mark.skip(reason="planned UIX boundary; runtime/API boundary intentionally excludes it")
def test_uix_tenant_jwks_publication_view_contract() -> None:
    raise AssertionError("planned")
