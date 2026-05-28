from __future__ import annotations

import os

import httpx
import pytest


pytestmark = pytest.mark.integration

BASE_URL = os.environ.get("TIGRBL_AUTH_MY_ACCOUNT_API_PROOF_URL", "http://localhost:8019")


def _require_live_my_account_api() -> None:
    try:
        response = httpx.get(f"{BASE_URL}/openapi.json", timeout=3.0)
    except httpx.HTTPError as exc:
        pytest.skip(f"My Account API dev deployment is not reachable at {BASE_URL}: {exc}")
    if response.status_code != 200:
        pytest.skip(
            f"My Account API dev deployment at {BASE_URL} returned "
            f"{response.status_code} for OpenAPI readiness"
        )


def test_my_account_api_dev_deployment_serves_current_subject_surface() -> None:
    _require_live_my_account_api()

    with httpx.Client(base_url=BASE_URL, timeout=10.0) as client:
        docs = client.get("/docs")
        openapi = client.get("/openapi.json")
        anonymous = client.get("/account/profile")
        rpc = client.post("/rpc", json={})

    assert docs.status_code == 200, docs.text
    assert openapi.status_code == 200, openapi.text
    assert anonymous.status_code == 401, anonymous.text
    assert rpc.status_code == 404, rpc.text
    paths = openapi.json()["paths"]
    assert "/account/profile" in paths
    assert "/account/sessions" in paths
    assert "/account/authorized-apps" in paths
    assert "/account/consents" in paths
    for forbidden in ("/admin/tenant", "/admin/identity", "/login", "/token", "/register", "/rpc"):
        assert forbidden not in paths
