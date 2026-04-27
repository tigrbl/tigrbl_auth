from tigrbl_auth.uix import AdminConsoleShell, AdminPrincipal, AdminSession, TenantProfileSelection


def test_admin_uix_golden_path_from_login_to_dashboard_to_mutation_audit():
    shell = AdminConsoleShell(issuer="https://issuer.example", environment_label="local")
    path = shell.golden_path(
        session=AdminSession(
            session_id="sess-admin",
            authenticated=True,
            principal=AdminPrincipal(subject="admin@example.com", roles=("admin",)),
        ),
        initial_selection=TenantProfileSelection(
            tenant_id="tenant-a",
            deployment_profile="baseline",
            surface_sets=("admin-rpc",),
        ),
        next_selection=TenantProfileSelection(
            tenant_id="tenant-b",
            deployment_profile="production",
            surface_sets=("admin-rpc", "diagnostics"),
        ),
    )

    assert path["principal_subject"] == "admin@example.com"
    assert [event["event"] for event in path["events"]] == [
        "admin.session.accepted",
        "admin.dashboard.rendered",
        "admin.context.selected",
        "admin.audit.recorded",
    ]
    assert path["events"][2]["tenant_id"] == "tenant-b"
    assert path["events"][2]["deployment_profile"] == "production"
