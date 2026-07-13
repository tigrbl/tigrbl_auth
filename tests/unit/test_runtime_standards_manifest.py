import sys
from pathlib import Path

from tigrbl_auth import standard_version, standards_manifest

sys.path.insert(
    0,
    str(
        Path(__file__).resolve().parents[2] / "pkgs/80-apis/tigrbl-auth-api-public/src"
    ),
)
from tigrbl_auth_api_public import PUBLIC_API_CONTRACT  # noqa: E402
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


def test_public_api_contract_consumes_runtime_protocol_truth() -> None:
    assert "standards-manifest" in PUBLIC_API_CONTRACT.production_capabilities
    assert "tigrbl-auth-protocol-oid4vci" in PUBLIC_API_CONTRACT.consumed_packages
    assert "tigrbl-auth-protocol-oid4vp" in PUBLIC_API_CONTRACT.consumed_packages
    assert "tigrbl-auth-profile-haip" in PUBLIC_API_CONTRACT.consumed_packages


def test_standards_manifest_is_mounted_from_runtime_capability_truth() -> None:
    deployment = resolve_deployment(product_surface="public-api")
    assert deployment.capability_enabled("standards-manifest")
    app = build_app(deployment=deployment)
    paths = {
        getattr(route, "path", None) or getattr(route, "path_template", None)
        for route in getattr(app, "_routes", ())
    }
    assert "/standards" in paths
