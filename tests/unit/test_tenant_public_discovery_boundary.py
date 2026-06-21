from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
from httpx import ASGITransport, AsyncClient

ROOT = Path(__file__).resolve().parents[2]
for src in sorted((ROOT / "pkgs").glob("**/src"), reverse=True):
    value = str(src)
    if value in sys.path:
        sys.path.remove(value)
    sys.path.insert(0, value)

import tigrbl_identity_principals as principals  # noqa: E402

from tigrbl_auth.api.app import build_app  # noqa: E402
from tigrbl_auth.cli.artifacts import build_openapi_contract, deployment_from_options, write_discovery_artifacts  # noqa: E402
from tigrbl_identity_storage.operator_store import OperationContext  # noqa: E402
from tigrbl_auth.services.operator_service import create_resource, generate_key_record, publish_jwks_document  # noqa: E402
from tigrbl_auth_protocol_oidc.tenant_discovery import (  # noqa: E402
    TENANT_JWKS_PATH,
    TENANT_OPENID_CONFIGURATION_PATH,
    require_tenant_issuer,
    resolve_tenant_trust_domain_authority,
    tenant_issuer,
)
from tigrbl_identity_storage.tables.tenant.operator_state import enabled_tenant_record  # noqa: E402


ROOT_ISSUER = "https://id.example.com"
TENANT_A = "tenant-a"
TENANT_B = "tenant-b"

BOUNDARY_FEATURE_IDS = {
    "feat:tenant-scoped-issuer-boundary",
    "feat:route-tenant-openid-configuration",
    "feat:route-tenant-jwks-json",
    "feat:tenant-discovery-jwks-uri",
    "feat:tenant-jwks-key-filtering",
    "feat:tenant-jwks-rotation-visibility",
    "feat:tenant-public-discovery-disabled-policy",
    "feat:operator-tenant-jwks-runtime-parity",
    "feat:openapi-tenant-discovery-routes",
    "feat:discovery-snapshot-tenant-profile-artifacts",
    "feat:tenant-issuer-token-validation-contract",
    "feat:tenant-jwks-cross-tenant-leakage-guard",
}

TENANT_PUBLIC_DISCOVERY_BOUNDARY = {
    "feat:tenant-scoped-issuer-boundary": {
        "category": "tenant-issuer",
        "runtime_objects": ("TenantTrustDomainAuthority", "tenant_issuer"),
        "guarded_capabilities": ("issuer-boundary", "tenant-scope"),
    },
    "feat:route-tenant-openid-configuration": {
        "category": "route",
        "runtime_objects": ("build_tenant_openid_config", "TENANT_OPENID_CONFIGURATION_PATH"),
        "guarded_capabilities": ("route-enabled", "tenant-exists"),
    },
    "feat:route-tenant-jwks-json": {
        "category": "route",
        "runtime_objects": ("TENANT_JWKS_PATH", "tenant_jwks_path"),
        "guarded_capabilities": ("route-enabled", "tenant-exists"),
    },
    "feat:tenant-discovery-jwks-uri": {
        "category": "discovery-document",
        "runtime_objects": ("build_tenant_openid_config", "tenant_jwks_path"),
        "guarded_capabilities": ("jwks-uri", "issuer-root"),
    },
    "feat:tenant-jwks-key-filtering": {
        "category": "jwks",
        "runtime_objects": ("TENANT_JWKS_PATH",),
        "guarded_capabilities": ("tenant-filtering", "public-key-only"),
    },
    "feat:tenant-jwks-rotation-visibility": {
        "category": "jwks",
        "runtime_objects": ("TENANT_JWKS_PATH",),
        "guarded_capabilities": ("active-visible", "next-visible", "retired-hidden"),
    },
    "feat:tenant-public-discovery-disabled-policy": {
        "category": "route-policy",
        "runtime_objects": ("enabled_tenant_record",),
        "guarded_capabilities": ("disabled-tenant-404", "missing-tenant-404"),
    },
    "feat:operator-tenant-jwks-runtime-parity": {
        "category": "operator-parity",
        "runtime_objects": ("TENANT_JWKS_PATH",),
        "guarded_capabilities": ("runtime-payload-parity",),
    },
    "feat:openapi-tenant-discovery-routes": {
        "category": "contract",
        "runtime_objects": ("TENANT_OPENID_CONFIGURATION_PATH", "TENANT_JWKS_PATH"),
        "guarded_capabilities": ("openapi-route-parameters",),
    },
    "feat:discovery-snapshot-tenant-profile-artifacts": {
        "category": "snapshot",
        "runtime_objects": ("build_tenant_openid_config",),
        "guarded_capabilities": ("tenant-profile-artifacts",),
    },
    "feat:tenant-issuer-token-validation-contract": {
        "category": "validation",
        "runtime_objects": ("require_tenant_issuer", "TenantTrustDomainAuthority"),
        "guarded_capabilities": ("accepted-issuer-only",),
    },
    "feat:tenant-jwks-cross-tenant-leakage-guard": {
        "category": "leakage-guard",
        "runtime_objects": ("build_tenant_openid_config",),
        "guarded_capabilities": ("cross-tenant-redaction", "tenant-path-isolation"),
    },
}


def _settings(tmp_path: Path) -> SimpleNamespace:
    return SimpleNamespace(admin_api_key="test-admin-key", admin_api_key_dir=str(tmp_path), issuer=ROOT_ISSUER)


def _deployment():
    return deployment_from_options(profile="production", issuer=ROOT_ISSUER)


def _context(tmp_path: Path, resource: str, command: str, *, tenant: str | None = None) -> OperationContext:
    return OperationContext(
        repo_root=tmp_path,
        command=command,
        resource=resource,
        actor="boundary",
        profile="production",
        tenant=tenant,
    )


def _seed_operator_records(tmp_path: Path) -> None:
    tenant_ctx = _context(tmp_path, "tenant", "tenant.create")
    create_resource(tenant_ctx, record_id=TENANT_A, patch={"name": "Tenant A"}, if_exists="error")
    create_resource(tenant_ctx, record_id=TENANT_B, patch={"name": "Tenant B"}, if_exists="error")
    create_resource(tenant_ctx, record_id="tenant-disabled", patch={"name": "Disabled", "enabled": False}, if_exists="error")

    generate_key_record(
        _context(tmp_path, "keys", "keys.generate", tenant=TENANT_A),
        patch={"kid": "kid-a-active", "status": "active", "x": "a-active"},
    )
    generate_key_record(
        _context(tmp_path, "keys", "keys.generate", tenant=TENANT_A),
        patch={"kid": "kid-a-next", "status": "next", "x": "a-next"},
    )
    generate_key_record(
        _context(tmp_path, "keys", "keys.generate", tenant=TENANT_A),
        patch={"kid": "kid-a-retired", "status": "retired", "x": "a-retired"},
    )
    generate_key_record(
        _context(tmp_path, "keys", "keys.generate", tenant=TENANT_B),
        patch={"kid": "kid-b-active", "status": "active", "x": "b-active"},
    )


async def _client(tmp_path: Path) -> AsyncClient:
    app = build_app(_settings(tmp_path), deployment=_deployment())
    return AsyncClient(transport=ASGITransport(app=app), base_url=ROOT_ISSUER)


def test_tenant_public_discovery_boundary_t0_inventory_tracks_all_features():
    categories = {row["category"] for row in TENANT_PUBLIC_DISCOVERY_BOUNDARY.values()}

    assert set(TENANT_PUBLIC_DISCOVERY_BOUNDARY) == BOUNDARY_FEATURE_IDS
    assert len(TENANT_PUBLIC_DISCOVERY_BOUNDARY) == 12
    assert {"tenant-issuer", "route", "jwks", "operator-parity", "contract", "snapshot", "validation", "leakage-guard"} <= categories
    assert TENANT_PUBLIC_DISCOVERY_BOUNDARY["feat:route-tenant-jwks-json"]["category"] == "route"
    assert TENANT_OPENID_CONFIGURATION_PATH == "/tenants/{tenant_slug}/.well-known/openid-configuration"
    assert TENANT_JWKS_PATH == "/tenants/{tenant_slug}/.well-known/jwks.json"
    assert enabled_tenant_record(Path.cwd(), "missing") is None
    assert not hasattr(principals, "TENANT_OPENID_CONFIGURATION_PATH")
    assert not hasattr(principals, "TENANT_JWKS_PATH")
    assert not hasattr(principals, "tenant_public_discovery_boundary_manifest")
    assert not hasattr(principals, "tenant_public_discovery_boundary_integrity")


@pytest.mark.asyncio
async def test_tenant_public_discovery_boundary_t1_composes_runtime_contracts(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("TIGRBL_AUTH_OPERATOR_STATE_DIR", str(tmp_path / ".operator-state"))
    monkeypatch.chdir(tmp_path)
    await asyncio.to_thread(_seed_operator_records, tmp_path)
    deployment = _deployment()
    authority = resolve_tenant_trust_domain_authority(deployment, TENANT_A)
    operator = await asyncio.to_thread(
        publish_jwks_document,
        _context(tmp_path, "keys", "keys.publish-jwks", tenant=TENANT_A),
    )
    operator_payload = json.loads((tmp_path / operator.path).read_text(encoding="utf-8"))
    contract = build_openapi_contract(deployment, version="0.0.0-test")
    artifacts = write_discovery_artifacts(tmp_path, deployment, profile_label="production")

    async with await _client(tmp_path) as client:
        discovery = await client.get(f"/tenants/{TENANT_A}/.well-known/openid-configuration")
        jwks = await client.get(f"/tenants/{TENANT_A}/.well-known/jwks.json")

    discovery_payload = discovery.json()
    jwks_payload = jwks.json()
    kids = {key["kid"] for key in jwks_payload["keys"]}
    snapshot = json.loads(artifacts["tenants/tenant-a/openid-configuration.json"].read_text(encoding="utf-8"))

    assert discovery.status_code == 200
    assert jwks.status_code == 200
    assert discovery_payload["issuer"] == tenant_issuer(ROOT_ISSUER, TENANT_A)
    assert discovery_payload["jwks_uri"] == f"{ROOT_ISSUER}/tenants/{TENANT_A}/.well-known/jwks.json"
    assert discovery_payload["tigrbl_auth_subject_namespace"] == f"{TENANT_A}:subjects"
    assert authority.accepted_issuers == (discovery_payload["issuer"],)
    assert jwks_payload == operator_payload
    assert {"kid-a-active", "kid-a-next"} <= kids
    assert "kid-a-retired" not in kids
    assert TENANT_OPENID_CONFIGURATION_PATH in contract["paths"]
    assert TENANT_JWKS_PATH in contract["paths"]
    assert snapshot["issuer"] == discovery_payload["issuer"]


@pytest.mark.asyncio
async def test_tenant_public_discovery_boundary_t2_fails_closed_for_disabled_policy_and_leakage(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setenv("TIGRBL_AUTH_OPERATOR_STATE_DIR", str(tmp_path / ".operator-state"))
    monkeypatch.chdir(tmp_path)
    await asyncio.to_thread(_seed_operator_records, tmp_path)

    async with await _client(tmp_path) as client:
        missing = await client.get("/tenants/missing/.well-known/openid-configuration")
        disabled = await client.get("/tenants/tenant-disabled/.well-known/jwks.json")
        tenant_a_discovery = await client.get(f"/tenants/{TENANT_A}/.well-known/openid-configuration")
        tenant_a_jwks = await client.get(f"/tenants/{TENANT_A}/.well-known/jwks.json")

    combined = json.dumps(
        {"discovery": tenant_a_discovery.json(), "jwks": tenant_a_jwks.json()},
        sort_keys=True,
    )

    assert missing.status_code == 404
    assert disabled.status_code == 404
    assert "kid-b-active" not in combined
    assert f"/tenants/{TENANT_B}" not in combined
    assert "kid-a-retired" not in combined

    require_tenant_issuer(
        {"iss": f"{ROOT_ISSUER}/tenants/{TENANT_A}"},
        root_issuer=ROOT_ISSUER,
        tenant_slug=TENANT_A,
    )
    with pytest.raises(ValueError, match="tenant token issuer mismatch"):
        require_tenant_issuer(
            {"iss": ROOT_ISSUER},
            root_issuer=ROOT_ISSUER,
            tenant_slug=TENANT_A,
        )
