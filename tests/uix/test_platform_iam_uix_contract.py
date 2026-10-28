from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_tenant_admin_exposes_customer_iam_routes() -> None:
    app = (ROOT / "pkgs/105-ui/tba-ui-tenant-admin/App.tsx").read_text(encoding="utf-8")
    for route in ("#/members", "#/groups", "#/roles", "#/grants", "#/effective-access", "#/access-reviews"):
        assert route in app
    assert "#/authority/break-glass" not in app


def test_platform_admin_exposes_internal_iam_and_idp_routes() -> None:
    app = (ROOT / "pkgs/105-ui/tba-ui-platform-admin/App.tsx").read_text(encoding="utf-8")
    for route in ("#/authority/people", "#/authority/grants", "#/authority/policies", "#/authority/decisions", "#/authority/break-glass", "#/identity-provider/clients"):
        assert route in app


def test_uix_consumes_layer_75_clients() -> None:
    tenant = (ROOT / "pkgs/105-ui/tba-ui-tenant-admin/package.json").read_text(encoding="utf-8")
    platform = (ROOT / "pkgs/105-ui/tba-ui-platform-admin/package.json").read_text(encoding="utf-8")
    assert "@tba/client-tenant-admin" in tenant
    assert "@tba/client-platform-admin" in platform
    assert "@tba/client-tenant-admin" in (ROOT / "pkgs/105-ui/tba-ui-tenant-admin/services/tenantAdminClient.ts").read_text(encoding="utf-8")
    assert "@tba/client-platform-admin" in (ROOT / "pkgs/105-ui/tba-ui-platform-admin/services/platformAdminClient.ts").read_text(encoding="utf-8")
