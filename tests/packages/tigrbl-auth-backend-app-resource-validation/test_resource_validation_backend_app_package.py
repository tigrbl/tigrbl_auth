from __future__ import annotations

import sys
from importlib import import_module
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest
from httpx import ASGITransport, AsyncClient

from tigrbl_auth.config.deployment import DEFAULT_VALUES, resolve_deployment


ROOT = Path(__file__).resolve().parents[3]
PKG_SRC = ROOT / "pkgs" / "tigrbl-auth-backend-app-resource-validation" / "src"
if str(PKG_SRC) not in sys.path:
    sys.path.insert(0, str(PKG_SRC))

resource_validation_package = import_module("tigrbl_auth_backend_app_resource_validation")
PRODUCT_SURFACE = resource_validation_package.PRODUCT_SURFACE
RESOURCE_VALIDATION_BACKEND_APP_CONTRACT = (
    resource_validation_package.RESOURCE_VALIDATION_BACKEND_APP_CONTRACT
)
build_app = resource_validation_package.build_app


def _settings(tmp_path: Path) -> SimpleNamespace:
    values = dict(DEFAULT_VALUES)
    values.update(
        deployment_profile="production",
        issuer="http://localhost:8014",
        protected_resource_identifier="http://localhost:8014/resource",
        require_tls=False,
        admin_api_key="test-admin-key",
        admin_api_key_dir=str(tmp_path),
        session_cookie_force_secure=False,
        enable_rfc9207=False,
    )
    return SimpleNamespace(**values)


def test_resource_validation_contract_matches_product_surface_registry() -> None:
    deployment = resolve_deployment(
        profile="production", product_surface=PRODUCT_SURFACE
    )

    assert PRODUCT_SURFACE == "resource-validation-app"
    assert RESOURCE_VALIDATION_BACKEND_APP_CONTRACT.product_surface == PRODUCT_SURFACE
    assert "tigrbl-authz-resource-server" in (
        RESOURCE_VALIDATION_BACKEND_APP_CONTRACT.intended_consumers
    )
    assert deployment.plugin_mode == "public-only"
    assert deployment.surface_enabled("public-rest")
    assert not deployment.surface_enabled("admin-rest")


def test_resource_validation_build_app_uses_environment_backed_default_settings() -> None:
    with patch.dict(
        "os.environ",
        {
            "AUTHN_ISSUER": "http://localhost:8014",
            "TIGRBL_AUTH_PROTECTED_RESOURCE_IDENTIFIER": (
                "http://localhost:8014/resource"
            ),
            "TIGRBL_AUTH_PROFILE": "production",
        },
    ):
        built = build_app()

    assert built.deployment.issuer == "http://localhost:8014"
    assert built.deployment.protected_resource_identifier == (
        "http://localhost:8014/resource"
    )
    assert built.deployment.product_surface == PRODUCT_SURFACE


def test_resource_validation_contract_routes_are_validation_only() -> None:
    deployment = resolve_deployment(
        profile="production", product_surface=PRODUCT_SURFACE
    )

    for capability in RESOURCE_VALIDATION_BACKEND_APP_CONTRACT.production_capabilities:
        assert deployment.capability_enabled(capability), capability

    for route in RESOURCE_VALIDATION_BACKEND_APP_CONTRACT.forbidden_exact_routes:
        assert route not in deployment.active_routes

    for prefix in RESOURCE_VALIDATION_BACKEND_APP_CONTRACT.forbidden_route_prefixes:
        assert all(
            not active_route.startswith(prefix)
            for active_route in deployment.active_routes
        )


def test_resource_validation_openapi_documents_introspection_only(
    tmp_path: Path,
) -> None:
    validation_app = build_app(_settings(tmp_path))
    openapi = validation_app.openapi()
    paths = openapi["paths"]

    assert "/introspect" in paths
    assert (
        "application/x-www-form-urlencoded"
        in paths["/introspect"]["post"]["requestBody"]["content"]
    )
    assert "/.well-known/openid-configuration" in paths
    assert "/.well-known/oauth-protected-resource" in paths
    assert "/.well-known/jwks.json" in paths
    assert "/metadata/capabilities" in paths
    assert "/metadata/verifier-contract" in paths

    for route in RESOURCE_VALIDATION_BACKEND_APP_CONTRACT.forbidden_exact_routes:
        assert route not in paths


@pytest.mark.asyncio
async def test_resource_validation_served_openapi_is_patched(
    tmp_path: Path,
) -> None:
    validation_app = build_app(_settings(tmp_path))

    async with AsyncClient(
        transport=ASGITransport(app=validation_app), base_url="http://test"
    ) as client:
        response = await client.get("/openapi.json")

    assert response.status_code == 200
    openapi = response.json()
    content = openapi["paths"]["/introspect"]["post"]["requestBody"]["content"]
    assert "application/x-www-form-urlencoded" in content


@pytest.mark.asyncio
async def test_resource_validation_metadata_endpoints_project_configured_behavior(
    tmp_path: Path,
) -> None:
    validation_app = build_app(_settings(tmp_path))

    async with AsyncClient(
        transport=ASGITransport(app=validation_app),
        base_url="http://localhost:8014",
    ) as client:
        jwks = await client.get("/.well-known/jwks.json")
        tenant_jwks = await client.get("/tenants/public/.well-known/jwks.json")
        resource_metadata = await client.get("/.well-known/oauth-protected-resource")
        issuer_metadata = await client.get("/.well-known/openid-configuration")
        capabilities = await client.get("/metadata/capabilities")
        verifier_contract = await client.get("/metadata/verifier-contract")
        missing_token = await client.post("/introspect", data={})

    assert jwks.status_code == 200
    assert "keys" in jwks.json()
    assert tenant_jwks.status_code == 200
    assert "keys" in tenant_jwks.json()

    assert resource_metadata.status_code == 200
    resource_payload = resource_metadata.json()
    assert resource_payload["resource"] == "http://localhost:8014/resource"
    assert resource_payload["authorization_servers"] == ["http://localhost:8014"]
    assert (
        resource_payload["jwks_uri"]
        == "http://localhost:8014/.well-known/jwks.json"
    )
    assert resource_payload["token_types_supported"] == ["access_token"]
    assert "bearer" in resource_payload["proof_modes_supported"]
    assert "introspection_endpoint_auth_methods_supported" in resource_payload

    assert issuer_metadata.status_code == 200
    issuer_payload = issuer_metadata.json()
    assert issuer_payload["issuer"] == "http://localhost:8014"
    assert issuer_payload["jwks_uri"] == "http://localhost:8014/.well-known/jwks.json"
    assert issuer_payload["introspection_endpoint"] == (
        "http://localhost:8014/introspect"
    )
    assert "tigrbl_auth_capabilities" in issuer_payload
    assert "introspection" in issuer_payload["tigrbl_auth_capabilities"]
    assert "token" not in issuer_payload["tigrbl_auth_capabilities"]

    assert capabilities.status_code == 200
    capabilities_payload = capabilities.json()
    assert capabilities_payload["product_surface"] == "resource-validation-app"
    assert capabilities_payload["artifact_sha256"]
    assert "introspection" in capabilities_payload["capabilities"]
    assert "evd:runtime-capability:introspection" in capabilities_payload["evidence_ids"]

    assert verifier_contract.status_code == 200
    verifier_payload = verifier_contract.json()
    assert verifier_payload["issuer"] == "http://localhost:8014"
    assert verifier_payload["jwks_uri"] == "http://localhost:8014/.well-known/jwks.json"
    assert verifier_payload["introspection_endpoint"] == "http://localhost:8014/introspect"
    assert verifier_payload["fail_closed"] is True

    assert missing_token.status_code == 400
    assert "token parameter required" in missing_token.text


@pytest.mark.asyncio
async def test_resource_validation_app_fails_closed_for_non_validation_paths(
    tmp_path: Path,
) -> None:
    validation_app = build_app(_settings(tmp_path))

    async with AsyncClient(
        transport=ASGITransport(app=validation_app), base_url="http://test"
    ) as client:
        login = await client.post("/login", json={})
        authorize = await client.get("/authorize")
        token = await client.post("/token", data={})
        register = await client.post("/register", json={})
        rpc = await client.post(
            "/rpc",
            json={"jsonrpc": "2.0", "method": "rpc.discover", "params": {}, "id": 1},
        )
        tenant = await client.get("/tenant")
        introspect = await client.post("/introspect", data={})

    assert login.status_code == 404
    assert authorize.status_code == 404
    assert token.status_code == 404
    assert register.status_code == 404
    assert rpc.status_code == 404
    assert tenant.status_code == 404
    assert introspect.status_code == 400
