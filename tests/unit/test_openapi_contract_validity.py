from __future__ import annotations

import json
from types import SimpleNamespace

import pytest
from httpx import ASGITransport, AsyncClient

from tigrbl_auth.api.app import build_app
from tigrbl_auth.api.surfaces import admin_resource_path_prefixes
from tigrbl_auth.cli.artifacts import build_openapi_contract, deployment_from_options
from tigrbl_auth.config.deployment import ROUTE_REGISTRY, resolve_deployment


PROFILES = ("baseline", "production", "hardening", "fapi2-security", "peer-claim")
DEFAULT_OPENAPI_DIALECT = "https://spec.openapis.org/oas/3.1/dialect/base"
JSON_SCHEMA_2020_12_DIALECT = "https://json-schema.org/draft/2020-12/schema"


def _expected_public_routes(deployment: object) -> set[str]:
    active_routes = set(getattr(deployment, "active_routes", ()))
    return {
        path
        for path in active_routes
        if ROUTE_REGISTRY.get(path, {}).get("surface_set") == "public-rest"
    }


def _assert_openapi_contract_valid(contract: dict, deployment: object) -> None:
    json.dumps(contract)

    assert str(contract.get("openapi", "")).startswith("3.")
    dialect = contract.get("jsonSchemaDialect")
    assert dialect in {None, DEFAULT_OPENAPI_DIALECT, JSON_SCHEMA_2020_12_DIALECT}
    assert contract.get("info", {}).get("title")
    assert contract.get("info", {}).get("version")
    assert contract.get("servers") == [{"url": getattr(deployment, "issuer")}]

    xmeta = contract.get("x-tigrbl-auth", {})
    assert xmeta.get("profile") == getattr(deployment, "profile")
    assert xmeta.get("plugin_mode") == getattr(deployment, "plugin_mode")

    expected_routes = _expected_public_routes(deployment)
    assert set(contract.get("paths", {})) == expected_routes
    assert contract.get("components", {}).get("schemas")

    security = contract.get("components", {}).get("securitySchemes", {})
    if deployment.flag_enabled("enable_rfc6750"):
        assert security["bearerAuth"]["scheme"] == "bearer"
    if deployment.flag_enabled("enable_rfc6749"):
        assert security["oauth2"]["type"] == "oauth2"
    if deployment.flag_enabled("enable_oidc_discovery"):
        assert security["openIdConnect"]["type"] == "openIdConnect"

    for path, operations in contract.get("paths", {}).items():
        route_meta = ROUTE_REGISTRY[path]
        assert set(operations) == set(route_meta.get("methods", ()))
        for method, operation in operations.items():
            assert operation["operationId"]
            assert operation["responses"]["200"]["description"] == "Success"
            assert operation["x-runtime-profile"]["profile"] == getattr(deployment, "profile")
            assert operation["x-required-flags"] == list(route_meta.get("flags", ()))
            assert method in route_meta.get("methods", ())


def _assert_runtime_openapi_payload_valid(payload: dict) -> None:
    json.dumps(payload)

    assert str(payload.get("openapi", "")).startswith("3.")
    dialect = payload.get("jsonSchemaDialect")
    assert dialect in {None, DEFAULT_OPENAPI_DIALECT, JSON_SCHEMA_2020_12_DIALECT}
    assert payload.get("info", {}).get("title")
    assert payload.get("info", {}).get("version")
    assert payload.get("paths")
    assert "/.well-known/openid-configuration" in payload["paths"]
    assert "/.well-known/jwks.json" in payload["paths"]


def _path_has_prefix(path: str, prefix: str) -> bool:
    return path == prefix or path.startswith(f"{prefix}/")


def _settings(tmp_path) -> SimpleNamespace:
    return SimpleNamespace(admin_api_key="test-admin-key", admin_api_key_dir=str(tmp_path))


@pytest.mark.parametrize("profile", PROFILES)
def test_openapi_builder_remains_valid_for_all_profiles(profile: str) -> None:
    deployment = deployment_from_options(profile=profile)
    contract = build_openapi_contract(deployment, version="0.0.0-test")
    _assert_openapi_contract_valid(contract, deployment)


@pytest.mark.parametrize("profile", PROFILES)
def test_openapi_builder_remains_valid_with_mixed_plugin_mode(profile: str) -> None:
    deployment = deployment_from_options(profile=profile, plugin_mode="mixed")
    contract = build_openapi_contract(deployment, version="0.0.0-test")
    _assert_openapi_contract_valid(contract, deployment)


@pytest.mark.asyncio
async def test_runtime_openapi_payload_remains_valid_for_public_only_runtime(tmp_path) -> None:
    deployment = resolve_deployment()
    app = build_app(_settings(tmp_path), deployment=deployment)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/openapi.json")

    assert response.status_code == 200
    payload = response.json()
    _assert_runtime_openapi_payload_valid(payload)
    assert not any(path.startswith("/system") for path in payload["paths"])
    assert not any(path.startswith("/rpc") for path in payload["paths"])
    assert not any(
        any(_path_has_prefix(path, prefix) for prefix in admin_resource_path_prefixes())
        for path in payload["paths"]
    )


@pytest.mark.asyncio
async def test_runtime_openapi_payload_remains_valid_for_mixed_runtime(tmp_path) -> None:
    deployment = resolve_deployment(plugin_mode="mixed")
    app = build_app(_settings(tmp_path), deployment=deployment)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/openapi.json")

    assert response.status_code == 200
    payload = response.json()
    _assert_runtime_openapi_payload_valid(payload)
    assert any(
        any(_path_has_prefix(path, prefix) for prefix in admin_resource_path_prefixes())
        for path in payload["paths"]
    )
    assert not any(path == "/rpc" or path.startswith("/rpc/") for path in payload["paths"])
