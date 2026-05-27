from __future__ import annotations

import os

import httpx
import pytest


pytestmark = pytest.mark.integration

BASE_URL = os.environ.get(
    "TIGRBL_AUTH_PLATFORM_ADMIN_API_PROOF_URL",
    "http://localhost:8015",
)
ADMIN_API_KEY = os.environ.get(
    "TIGRBL_AUTH_PLATFORM_ADMIN_API_PROOF_KEY",
    "dev-platform-admin-key",
)


def _client() -> httpx.Client:
    return httpx.Client(base_url=BASE_URL, timeout=10.0, follow_redirects=False)


def _require_live_platform_admin_api() -> None:
    try:
        response = httpx.get(f"{BASE_URL}/openapi.json", timeout=3.0)
    except httpx.HTTPError as exc:
        pytest.skip(
            f"platform-admin API dev deployment is not reachable at "
            f"{BASE_URL}: {exc}"
        )
    if response.status_code != 200:
        pytest.skip(
            f"platform-admin API dev deployment at {BASE_URL} returned "
            f"{response.status_code} for OpenAPI readiness"
        )


def test_platform_admin_api_dev_deployment_exposes_rest_control_plane_surface() -> None:
    _require_live_platform_admin_api()

    with _client() as client:
        openapi = client.get("/openapi.json")
        assert openapi.status_code == 200, openapi.text
        paths = openapi.json()["paths"]
        assert "/admin/tenant" in paths
        assert "/admin/tenant/{item_id}" in paths
        assert "/admin/identity" in paths
        assert "/admin/identity/{item_id}" in paths
        assert "/tenant" not in paths
        assert "/user" not in paths
        assert "/authsession" not in paths
        assert "/authsession/{item_id}" not in paths
        assert "/client" not in paths
        schemas = openapi.json()["components"]["schemas"]
        assert "TenantCreateRequest" in schemas
        assert "TenantUpdateRequest" in schemas
        assert "UserCreateRequest" in schemas
        assert "UserUpdateRequest" in schemas
        assert "AdminTenantProvisionIn" not in schemas
        assert "AdminIdentityProvisionIn" not in schemas
        assert (
            paths["/admin/tenant"]["post"]["requestBody"]["content"][
                "application/json"
            ]["schema"]["$ref"]
            == "#/components/schemas/TenantCreateRequest"
        )
        assert (
            paths["/admin/identity"]["post"]["requestBody"]["content"][
                "application/json"
            ]["schema"]["$ref"]
            == "#/components/schemas/UserCreateRequest"
        )
        for forbidden in (
            "/login",
            "/authorize",
            "/token",
            "/register",
            "/rpc",
            "/openrpc.json",
        ):
            assert forbidden not in paths

        openrpc = client.get("/openrpc.json")
        assert openrpc.status_code == 404, openrpc.text

        rpc = client.post(
            "/rpc",
            headers={"X-API-Key": ADMIN_API_KEY},
            json={},
        )
        assert rpc.status_code == 404, rpc.text

        invalid_key = client.get("/admin/tenant", headers={"X-API-Key": "wrong"})
        assert invalid_key.status_code == 403
        assert invalid_key.json()["error"] == "invalid_admin_api_key"
        raw_tenant = client.get("/tenant", headers={"X-API-Key": ADMIN_API_KEY})
        assert raw_tenant.status_code == 404, raw_tenant.text
        raw_user = client.get("/user", headers={"X-API-Key": ADMIN_API_KEY})
        assert raw_user.status_code == 404, raw_user.text
        raw_authsession = client.get(
            "/authsession", headers={"X-API-Key": ADMIN_API_KEY}
        )
        assert raw_authsession.status_code == 404, raw_authsession.text
        identity_missing_key = client.get("/admin/identity")
        assert identity_missing_key.status_code == 401
        assert identity_missing_key.json()["error"] == "missing_admin_api_key"

        for forbidden in ("/login", "/authorize", "/token", "/register"):
            response = client.post(forbidden)
            assert response.status_code == 404, forbidden
