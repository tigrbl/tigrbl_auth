from tigrbl_auth.uix import build_readiness_dashboard


def test_readiness_dashboard_renders_healthy_degraded_and_blocked_states():
    healthy = build_readiness_dashboard(
        {
            "admin_authorized": True,
            "readiness_healthy": True,
            "contracts_valid": True,
            "migrations_current": True,
            "cookies_secure": True,
            "openrpc_available": True,
        }
    )
    degraded = build_readiness_dashboard(
        {
            "admin_authorized": True,
            "readiness_healthy": False,
            "contracts_valid": True,
            "migrations_current": True,
            "cookies_secure": True,
            "openrpc_available": True,
        }
    )
    blocked = build_readiness_dashboard(
        {
            "admin_authorized": True,
            "readiness_healthy": True,
            "contracts_valid": False,
            "migrations_current": True,
            "cookies_secure": True,
            "openrpc_available": True,
        }
    )

    assert healthy.status == "healthy"
    assert degraded.status == "degraded"
    assert blocked.status == "blocked"


def test_readiness_dashboard_shows_runtime_database_issuer_key_and_gate_status():
    dashboard = build_readiness_dashboard(
        {
            "admin_authorized": True,
            "readiness_healthy": True,
            "contracts_valid": True,
            "migrations_current": False,
            "cookies_secure": True,
            "openrpc_available": True,
        },
        diagnostics={"issuer": "https://issuer.example", "client_secret": "secret"},
    )

    assert dashboard.sections == {
        "runtime": "ready",
        "database": "blocked",
        "issuer": "ready",
        "key_material": "ready",
        "admin_gate": "ready",
        "cookie_tls": "ready",
    }
    assert dashboard.diagnostics["client_secret"] == "[REDACTED]"
