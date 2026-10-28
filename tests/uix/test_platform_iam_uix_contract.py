from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_tenant_admin_exposes_customer_iam_routes() -> None:
    app = (ROOT / "pkgs/105-ui/tba-ui-tenant-administration/App.tsx").read_text(encoding="utf-8")
    for route in ("#/members", "#/groups", "#/roles", "#/grants", "#/effective-access", "#/access-reviews"):
        assert route in app
    assert "#/authority/break-glass" not in app


def test_platform_admin_exposes_internal_iam_and_idp_routes() -> None:
    app = (ROOT / "pkgs/105-ui/tba-ui-platform-administration/App.tsx").read_text(encoding="utf-8")
    for route in ("#/authority/people", "#/authority/grants", "#/authority/policies", "#/authority/decisions", "#/authority/break-glass", "#/identity-provider/clients"):
        assert route in app


def test_uix_consumes_layer_75_clients() -> None:
    tenant = (ROOT / "pkgs/105-ui/tba-ui-tenant-administration/package.json").read_text(encoding="utf-8")
    platform = (ROOT / "pkgs/105-ui/tba-ui-platform-administration/package.json").read_text(encoding="utf-8")
    assert "@tba/client-tenant-administration" in tenant
    assert "@tba/client-platform-administration" in platform
    assert "@tba/client-tenant-administration" in (ROOT / "pkgs/105-ui/tba-ui-tenant-administration/services/tenantAdminClient.ts").read_text(encoding="utf-8")
    assert "@tba/client-platform-administration" in (ROOT / "pkgs/105-ui/tba-ui-platform-administration/services/platformAdminClient.ts").read_text(encoding="utf-8")
