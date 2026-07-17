from __future__ import annotations

import os

import httpx
import pytest


pytestmark = pytest.mark.integration

BASE_URL = os.environ.get(
    "TIGRBL_AUTH_RESOURCE_VALIDATION_API_PROOF_URL",
    "http://localhost:8014",
)


def _client() -> httpx.Client:
    return httpx.Client(base_url=BASE_URL, timeout=10.0, follow_redirects=False)


def _require_live_resource_validation_api() -> None:
    try:
        response = httpx.get(f"{BASE_URL}/.well-known/jwks.json", timeout=3.0)
    except httpx.HTTPError as exc:
        pytest.skip(
            f"resource-validation API dev deployment is not reachable at "
            f"{BASE_URL}: {exc}"
        )
    if response.status_code != 200:
        pytest.skip(
            f"resource-validation API dev deployment at {BASE_URL} returned "
            f"{response.status_code} for JWKS readiness"
        )


def test_resource_validation_api_dev_deployment_exposes_validation_surface() -> None:
    _require_live_resource_validation_api()

    with _client() as client:
        jwks = client.get("/.well-known/jwks.json")
        assert jwks.status_code == 200, jwks.text
        assert "keys" in jwks.json()

        resource_metadata = client.get("/.well-known/oauth-protected-resource")
        assert resource_metadata.status_code == 200, resource_metadata.text
        resource_payload = resource_metadata.json()
        assert resource_payload["resource"] == f"{BASE_URL}/resource"
        assert resource_payload["authorization_servers"] == [BASE_URL]
        assert resource_payload["jwks_uri"] == f"{BASE_URL}/.well-known/jwks.json"
        assert "introspection_endpoint_auth_methods_supported" in resource_payload

        issuer_metadata = client.get("/.well-known/openid-configuration")
        assert issuer_metadata.status_code == 200, issuer_metadata.text
        issuer_payload = issuer_metadata.json()
        assert issuer_payload["issuer"] == BASE_URL
        assert issuer_payload["jwks_uri"] == f"{BASE_URL}/.well-known/jwks.json"
        assert issuer_payload["introspection_endpoint"] == f"{BASE_URL}/introspect"

        openapi = client.get("/openapi.json")
        assert openapi.status_code == 200, openapi.text
        paths = openapi.json()["paths"]
        assert "/introspect" in paths
        assert (
            "application/x-www-form-urlencoded"
            in paths["/introspect"]["post"]["requestBody"]["content"]
        )
        assert "/.well-known/oauth-protected-resource" in paths
        assert "/.well-known/jwks.json" in paths

        for forbidden in ("/login", "/authorize", "/token", "/register", "/rpc"):
            assert forbidden not in paths

        missing_token = client.post("/introspect", data={})
        assert missing_token.status_code == 400
        assert "token parameter required" in missing_token.text

        for forbidden in ("/login", "/authorize", "/token", "/register", "/rpc"):
            response = client.post(forbidden)
            assert response.status_code == 404, forbidden
