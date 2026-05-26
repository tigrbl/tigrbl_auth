from __future__ import annotations

import os

import httpx
import pytest


pytestmark = pytest.mark.integration

BASE_URL = os.environ.get(
    "TIGRBL_AUTH_DEVELOPER_API_PROOF_URL",
    "http://localhost:8017",
)
ADMIN_API_KEY = os.environ.get(
    "TIGRBL_AUTH_DEVELOPER_API_PROOF_KEY",
    "dev-developer-key",
)


def _client() -> httpx.Client:
    return httpx.Client(base_url=BASE_URL, timeout=10.0, follow_redirects=False)


def _require_live_developer_api() -> None:
    try:
        response = httpx.get(f"{BASE_URL}/openrpc.json", timeout=3.0)
    except httpx.HTTPError as exc:
        pytest.skip(
            f"developer API dev deployment is not reachable at {BASE_URL}: {exc}"
        )
    if response.status_code != 200:
        pytest.skip(
            f"developer API dev deployment at {BASE_URL} returned "
            f"{response.status_code} for OpenRPC readiness"
        )


def _method_names(openrpc: dict[str, object]) -> set[str]:
    return {str(item["name"]) for item in openrpc.get("methods", [])}


def _rpc_discover_method_names(result: dict[str, object]) -> set[str]:
    return {str(item["name"]) for item in result.get("methods", [])}


def test_developer_api_dev_deployment_exposes_client_registration_surface() -> None:
    _require_live_developer_api()

    with _client() as client:
        openapi = client.get("/openapi.json")
        assert openapi.status_code == 200, openapi.text
        paths = openapi.json()["paths"]
        assert "/register" in paths
        assert "/.well-known/openid-configuration" in paths
        assert "/.well-known/jwks.json" in paths
        assert "/client" in paths
        assert "/clientregistration" in paths
        assert "/auditevent" in paths
        for forbidden in (
            "/tenant",
            "/user",
            "/service",
            "/login",
            "/authorize",
            "/token",
            "/introspect",
        ):
            assert forbidden not in paths

        openrpc = client.get("/openrpc.json")
        assert openrpc.status_code == 200, openrpc.text
        methods = _method_names(openrpc.json())
        assert {"Client.list", "ClientRegistration.list", "AuditEvent.list"}.issubset(
            methods
        )
        assert "Tenant.list" not in methods
        assert "User.list" not in methods
        assert "Service.list" not in methods

        missing_key = client.post(
            "/rpc",
            json={"jsonrpc": "2.0", "method": "rpc.discover", "params": {}, "id": 1},
        )
        assert missing_key.status_code == 401
        assert missing_key.json()["error"] == "missing_admin_api_key"

        valid_key = client.post(
            "/rpc",
            headers={"X-API-Key": ADMIN_API_KEY},
            json={"jsonrpc": "2.0", "method": "rpc.discover", "params": {}, "id": 1},
        )
        assert valid_key.status_code == 200, valid_key.text
        result = valid_key.json()["result"]
        assert result["deployment"]["plugin_mode"] == "mixed"
        assert result["deployment"]["surface_sets"] == ["public-rest", "admin-rpc"]
        assert "/register" in result["deployment"]["active_routes"]
        assert "client.registration.upsert" in (
            result["deployment"]["active_openrpc_methods"]
        )
        rpc_methods = _rpc_discover_method_names(result)
        assert "client.list" in rpc_methods
        assert "client.registration.upsert" in rpc_methods
        assert "tenant.list" not in rpc_methods
        assert "identity.list" not in rpc_methods
        assert "token.inspect" not in rpc_methods

        invalid_key = client.get("/client", headers={"X-API-Key": "wrong"})
        assert invalid_key.status_code == 403
        assert invalid_key.json()["error"] == "invalid_admin_api_key"

        register = client.post("/register", json={})
        assert register.status_code != 404

        for forbidden in (
            "/tenant",
            "/user",
            "/service",
            "/login",
            "/authorize",
            "/token",
            "/introspect",
        ):
            response = client.post(forbidden)
            assert response.status_code == 404, forbidden
