import sys
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient

from tigrbl_auth import standard_version, standards_manifest

sys.path.insert(
    0,
    str(
        Path(__file__).resolve().parents[2] / "pkgs/90-backend-apps/tigrbl-auth-backend-app-public/src"
    ),
)
from tigrbl_auth_backend_app_public import PUBLIC_BACKEND_APP_CONTRACT  # noqa: E402
from tigrbl_identity_runtime.deployment import resolve_deployment
from tigrbl_identity_server.api.app import build_app


def test_runtime_manifest_exposes_exact_protocol_owner_versions() -> None:
    manifest = {item["family"]: item for item in standards_manifest()}
    assert manifest["oid4vci"]["version"] == "1.0"
    assert manifest["oid4vp"]["version"] == "1.0"
    assert manifest["haip"]["version"] == "1.0"
    assert manifest["set"]["version"] == "RFC8417"
    assert manifest["eat"]["version"] == "RFC9711"
    assert manifest["sd-jwt-vc"]["status"] == "active-draft"
    assert standard_version("gnap").version == "RFC9635"


def test_public_backend_app_contract_consumes_runtime_protocol_truth() -> None:
    assert "standards-manifest" in PUBLIC_BACKEND_APP_CONTRACT.production_capabilities
    assert "tigrbl-auth-protocol-oid4vci" in PUBLIC_BACKEND_APP_CONTRACT.consumed_packages
    assert "tigrbl-auth-protocol-oid4vp" in PUBLIC_BACKEND_APP_CONTRACT.consumed_packages
    assert "tigrbl-auth-profile-haip" in PUBLIC_BACKEND_APP_CONTRACT.consumed_packages


def test_standards_manifest_is_mounted_from_runtime_capability_truth() -> None:
    deployment = resolve_deployment(product_surface="public-app")
    assert deployment.capability_enabled("standards-manifest")
    app = build_app(deployment=deployment)
    paths = {
        getattr(route, "path", None) or getattr(route, "path_template", None)
        for route in getattr(app, "_routes", ())
    }
    assert "/standards" in paths


@pytest.mark.anyio
async def test_advanced_protocol_routes_are_mounted_and_fail_closed_without_components() -> (
    None
):
    app = build_app(deployment=resolve_deployment(product_surface="public-app"))
    requests = (
        (
            "/credential",
            {"credential_configuration_id": "employee", "format": "dc+sd-jwt"},
        ),
        (
            "/presentation/verify",
            {
                "holder": "holder",
                "vp_token": "token",
                "authorization_request": {
                    "client_id": "verifier",
                    "nonce": "nonce",
                    "accepted_formats": ["dc+sd-jwt"],
                },
            },
        ),
        (
            "/access/v1/evaluation",
            {
                "subject": {"type": "user", "id": "alice"},
                "action": {"type": "action", "id": "read"},
                "resource": {"type": "document", "id": "one"},
            },
        ),
        ("/gnap/tx", {"access_token": {"access": ["read"]}, "client": "key"}),
        ("/security-events/receive", {"set": "encoded"}),
        ("/attestations/appraise", {"profile": "eat", "claims": {}}),
    )
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        for path, payload in requests:
            response = await client.post(path, json=payload)
            assert response.status_code == 503, (path, response.text)
