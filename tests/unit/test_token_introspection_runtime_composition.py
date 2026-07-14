from __future__ import annotations

from types import SimpleNamespace

from tigrbl_identity_server.security.token_introspection import (
    build_rfc7662_introspection_service,
    token_introspection,
)
from tigrbl_identity_storage_runtime.token_lifecycle import introspect_token_async


def test_runtime_composes_durable_lookup_as_reportable_capability() -> None:
    report = token_introspection.capability_report()

    assert report["capability_id"] == "token.introspection"
    assert report["bound_operations"] == ("introspect_token",)
    assert token_introspection._introspect_token is introspect_token_async


def test_runtime_composes_protocol_feature_state_without_global_capture() -> None:
    enabled = build_rfc7662_introspection_service(
        SimpleNamespace(enable_rfc7662=True)
    )
    disabled = build_rfc7662_introspection_service(
        SimpleNamespace(enable_rfc7662=False)
    )

    assert enabled.capability is token_introspection
    assert enabled.enabled is True
    assert disabled.capability is token_introspection
    assert disabled.enabled is False
