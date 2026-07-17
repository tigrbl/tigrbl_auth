from __future__ import annotations

import os

import httpx
import pytest


pytestmark = pytest.mark.integration

BASE_URL = os.environ.get(
    "TIGRBL_AUTH_TENANT_ADMIN_API_PROOF_URL",
    "http://localhost:8016",
)
ADMIN_API_KEY = os.environ.get(
    "TIGRBL_AUTH_TENANT_ADMIN_API_PROOF_KEY",
    "dev-tenant-admin-key",
)


def _client() -> httpx.Client:
    return httpx.Client(base_url=BASE_URL, timeout=10.0, follow_redirects=False)


def _require_live_tenant_admin_api() -> None:
    try:
        response = httpx.get(f"{BASE_URL}/openapi.json", timeout=3.0)
    except httpx.HTTPError as exc:
        pytest.skip(
            f"tenant-admin API dev deployment is not reachable at "
            f"{BASE_URL}: {exc}"
        )
    if response.status_code != 200:
        pytest.skip(
            f"tenant-admin API dev deployment at {BASE_URL} returned "
            f"{response.status_code} for OpenAPI readiness"
        )


def test_tenant_admin_api_dev_deployment_exposes_tenant_control_plane() -> None:
    _require_live_tenant_admin_api()

    with _client() as client:
        openapi = client.get("/openapi.json")
        assert openapi.status_code == 200, openapi.text
        paths = openapi.json()["paths"]
        assert "/user" in paths
        assert "/client" in paths
        assert "/clientregistration" in paths
        assert "/consent" in paths
        assert "/authsession" not in paths
        assert "/tenant" not in paths
        assert "/service" not in paths
        for forbidden in ("/login", "/authorize", "/token", "/register"):
            assert forbidden not in paths

        openrpc = client.get("/openrpc.json")
        assert openrpc.status_code == 404, openrpc.text

        missing_key = client.post(
            "/rpc",
            json={"jsonrpc": "2.0", "method": "rpc.discover", "params": {}, "id": 1},
        )
        assert missing_key.status_code == 404

        valid_key = client.post(
            "/rpc",
            headers={"X-API-Key": ADMIN_API_KEY},
            json={"jsonrpc": "2.0", "method": "rpc.discover", "params": {}, "id": 1},
        )
        assert valid_key.status_code == 404, valid_key.text

        invalid_key = client.get("/user", headers={"X-API-Key": "wrong"})
        assert invalid_key.status_code == 403
        assert invalid_key.json()["error"] == "invalid_admin_api_key"

        for forbidden in (
            "/tenant",
            "/service",
            "/login",
            "/authorize",
            "/token",
            "/register",
        ):
            response = client.post(forbidden)
            assert response.status_code == 404, forbidden
