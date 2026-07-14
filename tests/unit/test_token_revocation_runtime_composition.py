from __future__ import annotations

from types import SimpleNamespace

from tigrbl_identity_server.security.token_revocation import (
    build_rfc7009_revocation_service,
    token_revocation,
)


def test_runtime_composes_durable_revocation_and_audit_operations() -> None:
    report = token_revocation.capability_report()

    assert report["capability_id"] == "token.revocation"
    assert report["bound_operations"] == (
        "record_audit_event",
        "revoke_token",
    )
    assert token_revocation.state().details == {"audit_bound": True}


def test_runtime_composes_rfc7009_feature_state() -> None:
    enabled = build_rfc7009_revocation_service(
        SimpleNamespace(enable_rfc7009=True)
    )
    disabled = build_rfc7009_revocation_service(
        SimpleNamespace(enable_rfc7009=False)
    )

    assert enabled.capability is token_revocation
    assert enabled.enabled is True
    assert disabled.enabled is False
