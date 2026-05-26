from __future__ import annotations

import os
from urllib.parse import parse_qs, urlparse
from uuid import uuid4

import httpx
import pytest


pytestmark = pytest.mark.integration

BASE_URL = os.environ.get("TIGRBL_AUTH_PUBLIC_API_PROOF_URL", "http://localhost:8013")
ADMIN_USERNAME = os.environ.get("TIGRBL_AUTH_PUBLIC_API_PROOF_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get(
    "TIGRBL_AUTH_PUBLIC_API_PROOF_PASSWORD", "AdminPass123!"
)
REDIRECT_URI = os.environ.get(
    "TIGRBL_AUTH_PUBLIC_API_PROOF_REDIRECT_URI",
    "http://127.0.0.1:8080/callback",
)
PKCE_VERIFIER = "dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk"
PKCE_CHALLENGE = "E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM"


def _client() -> httpx.Client:
    return httpx.Client(base_url=BASE_URL, timeout=10.0, follow_redirects=False)


def _require_live_public_api() -> None:
    try:
        response = httpx.get(f"{BASE_URL}/.well-known/jwks.json", timeout=3.0)
    except httpx.HTTPError as exc:
        pytest.skip(f"public API dev deployment is not reachable at {BASE_URL}: {exc}")
    if response.status_code != 200:
        pytest.skip(
            f"public API dev deployment at {BASE_URL} returned "
            f"{response.status_code} for JWKS readiness"
        )


def _register_client(
    client: httpx.Client,
    *,
    grant_types: list[str],
    client_name: str,
) -> dict[str, object]:
    response = client.post(
        "/register",
        json={
            "tenant_slug": "public",
            "redirect_uris": [REDIRECT_URI],
            "grant_types": grant_types,
            "response_types": ["code"],
            "token_endpoint_auth_method": "client_secret_post",
            "client_name": f"{client_name}-{uuid4().hex[:8]}",
            "scope": "openid profile email",
        },
    )
    assert response.status_code == 200, response.text
    payload = response.json()
    assert payload["client_id"]
    assert payload["client_secret"]
    return payload


def test_public_api_dev_deployment_supports_documented_auth_flows() -> None:
    _require_live_public_api()

    with _client() as client:
        discovery = client.get("/.well-known/openid-configuration")
        assert discovery.status_code == 200, discovery.text
        metadata = discovery.json()
        assert metadata["issuer"] == BASE_URL
        assert metadata["authorization_endpoint"] == f"{BASE_URL}/authorize"
        assert metadata["token_endpoint"] == f"{BASE_URL}/token"

        openapi = client.get("/openapi.json")
        assert openapi.status_code == 200, openapi.text
        paths = openapi.json()["paths"]
        assert paths["/login"]["post"]["requestBody"]["content"][
            "application/json"
        ]
        assert paths["/register"]["post"]["requestBody"]["content"][
            "application/json"
        ]
        assert (
            "application/x-www-form-urlencoded"
            in paths["/token"]["post"]["requestBody"]["content"]
        )
        authorize_param_names = {
            item["name"] for item in paths["/authorize"]["get"]["parameters"]
        }
        assert {
            "response_type",
            "client_id",
            "redirect_uri",
            "code_challenge",
            "code_challenge_method",
        }.issubset(authorize_param_names)

        login = client.post(
            "/login",
            json={"identifier": ADMIN_USERNAME, "password": ADMIN_PASSWORD},
        )
        assert login.status_code == 200, login.text
        login_payload = login.json()
        assert login_payload["access_token"]
        assert login_payload["token_type"] == "bearer"
        assert "sid" in client.cookies

        password_client = _register_client(
            client,
            grant_types=["authorization_code", "refresh_token", "password"],
            client_name="proof-password-client",
        )
        password_token = client.post(
            "/token",
            data={
                "grant_type": "password",
                "client_id": password_client["client_id"],
                "client_secret": password_client["client_secret"],
                "username": ADMIN_USERNAME,
                "password": ADMIN_PASSWORD,
                "scope": "openid profile email",
            },
        )
        assert password_token.status_code == 200, password_token.text
        password_token_payload = password_token.json()
        assert password_token_payload["token_type"] == "bearer"
        assert password_token_payload["access_token"]
        assert password_token_payload["refresh_token"]

        code_client = _register_client(
            client,
            grant_types=["authorization_code", "refresh_token"],
            client_name="proof-auth-code-client",
        )
        authorize = client.get(
            "/authorize",
            params={
                "response_type": "code",
                "client_id": code_client["client_id"],
                "redirect_uri": REDIRECT_URI,
                "scope": "openid profile email",
                "state": "proof-state",
                "nonce": "proof-nonce",
                "code_challenge": PKCE_CHALLENGE,
                "code_challenge_method": "S256",
            },
        )
        assert authorize.status_code in {302, 307}, authorize.text
        location = authorize.headers["location"]
        parsed = urlparse(location)
        params = parse_qs(parsed.query)
        assert parsed.scheme in {"http", "https"}
        assert params["state"] == ["proof-state"]
        auth_code = params["code"][0]
        assert auth_code

        code_token = client.post(
            "/token",
            data={
                "grant_type": "authorization_code",
                "client_id": code_client["client_id"],
                "client_secret": code_client["client_secret"],
                "code": auth_code,
                "redirect_uri": REDIRECT_URI,
                "code_verifier": PKCE_VERIFIER,
            },
        )
        assert code_token.status_code == 200, code_token.text
        code_token_payload = code_token.json()
        assert code_token_payload["token_type"] == "bearer"
        assert code_token_payload["access_token"]
        assert code_token_payload["refresh_token"]
