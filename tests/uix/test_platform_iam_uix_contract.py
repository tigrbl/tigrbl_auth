from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_tenant_admin_exposes_customer_iam_routes() -> None:
    app = (ROOT / "pkgs/105-ui/tenant-admin-uix/App.tsx").read_text(encoding="utf-8")
    for route in ("#/members", "#/groups", "#/roles", "#/grants", "#/effective-access", "#/access-reviews"):
        assert route in app
    assert "#/authority/break-glass" not in app


def test_platform_admin_exposes_internal_iam_and_idp_routes() -> None:
    app = (ROOT / "pkgs/105-ui/platform-admin-uix/App.tsx").read_text(encoding="utf-8")
    for route in ("#/authority/people", "#/authority/grants", "#/authority/policies", "#/authority/decisions", "#/authority/break-glass", "#/identity-provider/clients"):
        assert route in app


def test_uix_consumes_layer_75_clients() -> None:
    tenant = (ROOT / "pkgs/105-ui/tenant-admin-uix/package.json").read_text(encoding="utf-8")
    platform = (ROOT / "pkgs/105-ui/platform-admin-uix/package.json").read_text(encoding="utf-8")
    assert "@tigrbl-auth/tenant-admin-client" in tenant
    assert "@tigrbl-auth/platform-admin-client" in platform
    assert "@tigrbl-auth/tenant-admin-client" in (ROOT / "pkgs/105-ui/tenant-admin-uix/services/tenantAdminClient.ts").read_text(encoding="utf-8")
    assert "@tigrbl-auth/platform-admin-client" in (ROOT / "pkgs/105-ui/platform-admin-uix/services/platformAdminClient.ts").read_text(encoding="utf-8")
