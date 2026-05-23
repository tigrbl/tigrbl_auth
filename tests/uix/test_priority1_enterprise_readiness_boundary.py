from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OPERATOR_SRC = ROOT / "pkgs" / "tigrbl-identity-operator" / "src"
if str(OPERATOR_SRC) not in sys.path:
    sys.path.append(str(OPERATOR_SRC))

import tigrbl_identity_operator.uix as operator_uix  # noqa: E402

from tigrbl_auth.uix import (  # noqa: E402
    ENTERPRISE_READINESS_FEATURES,
    build_readiness_dashboard,
    enterprise_readiness_boundary_integrity,
    enterprise_readiness_boundary_manifest,
    redact_sensitive_values,
)


BOUNDARY_FEATURE_IDS = {
    "feat:uix-enterprise-readiness-dashboard",
    "feat:uix-redacted-config-viewer",
}


def _readiness(**overrides: bool) -> dict[str, bool]:
    values = {
        "admin_authorized": True,
        "readiness_healthy": True,
        "contracts_valid": True,
        "migrations_current": True,
        "cookies_secure": True,
        "openrpc_available": True,
    }
    values.update(overrides)
    return values


def test_priority1_enterprise_readiness_boundary_t0_inventory_tracks_all_features():
    manifest = enterprise_readiness_boundary_manifest()
    integrity = enterprise_readiness_boundary_integrity()
    operator_manifest = operator_uix.enterprise_readiness_boundary_manifest()
    operator_integrity = operator_uix.enterprise_readiness_boundary_integrity()

    assert set(manifest) == BOUNDARY_FEATURE_IDS
    assert set(ENTERPRISE_READINESS_FEATURES) == BOUNDARY_FEATURE_IDS
    assert manifest == operator_manifest
    assert integrity["passed"] is True
    assert operator_integrity["passed"] is True
    assert integrity["feature_count"] == 2
    assert set(integrity["surfaces"]) == {"readiness-dashboard", "redacted-config-viewer"}


def test_priority1_enterprise_readiness_boundary_t1_composes_dashboard_and_redaction():
    dashboard = build_readiness_dashboard(
        _readiness(),
        diagnostics={
            "issuer": "https://issuer.example.test",
            "client_secret": "secret-value",
            "database": {"host": "localhost", "password": "db-secret"},
        },
    )

    assert dashboard.status == "healthy"
    assert dashboard.warnings == ()
    assert dashboard.sections == {
        "runtime": "ready",
        "database": "ready",
        "issuer": "ready",
        "key_material": "ready",
        "admin_gate": "ready",
        "cookie_tls": "ready",
    }
    assert dashboard.diagnostics["issuer"] == "https://issuer.example.test"
    assert dashboard.diagnostics["client_secret"] == "[REDACTED]"
    assert dashboard.diagnostics["database"]["host"] == "localhost"
    assert dashboard.diagnostics["database"]["password"] == "[REDACTED]"


def test_priority1_enterprise_readiness_boundary_t2_blocks_and_redacts_unsafe_posture():
    degraded = build_readiness_dashboard(_readiness(readiness_healthy=False, cookies_secure=False))
    blocked = build_readiness_dashboard(
        _readiness(admin_authorized=False, contracts_valid=False, migrations_current=False),
        diagnostics={
            "jwt_secret": "secret",
            "api_token": "token",
            "nested": {"private_key": "key", "safe": "visible"},
        },
    )
    redacted = redact_sensitive_values(
        {
            "password": "pw",
            "not_secret": "visible",
            "nested": {"client_secret": "hidden", "host": "db"},
        }
    )

    assert degraded.status == "degraded"
    assert {warning.code for warning in degraded.warnings} == {"readiness_healthy", "cookies_secure"}
    assert blocked.status == "blocked"
    assert blocked.sections["admin_gate"] == "blocked"
    assert blocked.sections["database"] == "blocked"
    assert blocked.sections["issuer"] == "blocked"
    assert blocked.diagnostics["jwt_secret"] == "[REDACTED]"
    assert blocked.diagnostics["api_token"] == "[REDACTED]"
    assert blocked.diagnostics["nested"]["private_key"] == "[REDACTED]"
    assert blocked.diagnostics["nested"]["safe"] == "visible"
    assert redacted == {
        "password": "[REDACTED]",
        "not_secret": "visible",
        "nested": {"client_secret": "[REDACTED]", "host": "db"},
    }
