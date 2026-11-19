from __future__ import annotations
from tba_auth.services.governance_extension_plane import (
    PluginRuntimeRegistry,
    SDKEcosystemCatalog,
)


def test_sdk_ecosystem_tracks_runtime_compatibility_and_contract_alignment():
    catalog = SDKEcosystemCatalog()
    catalog.register_sdk(
        "sdk-python",
        package_name="tba-auth-python",
        language="python",
        version="0.3.4",
        compatible_runtime_range=("0.3.0", "0.3.9"),
        generated_contracts={"openapi": "3.1.0", "openrpc": "1.3.2"},
        auth_helpers=("pkce", "client_secret_basic"),
        supported_errors=("problem+json",),
    )
    catalog.register_sdk(
        "sdk-typescript",
        package_name="tba-auth-ts",
        language="typescript",
        version="0.3.4",
        compatible_runtime_range=("0.3.0", "0.3.9"),
        generated_contracts={"openapi": "3.1.0", "openrpc": "1.3.2"},
        auth_helpers=("pkce", "refresh_token"),
        supported_errors=("problem+json", "json-rpc"),
    )

    assert catalog.compatible_sdk_ids(runtime_version="0.3.4") == (
        "sdk-python",
        "sdk-typescript",
    )

    report = catalog.build_alignment_report(
        runtime_version="0.3.4",
        expected_contracts={"openapi": "3.1.0", "openrpc": "1.3.2"},
    )

    assert report["aligned_sdk_ids"] == ["sdk-python", "sdk-typescript"]
    assert report["mismatches"] == {}


def test_plugin_runtime_registry_enforces_isolation_audit_and_operator_controls():
    registry = PluginRuntimeRegistry()
    registry.register_plugin(
        "plugin-audit-export",
        name="Audit Export",
        version="1.0.0",
        extension_points=("audit.export", "entitlement.snapshot"),
        hooks={"before-export": lambda payload: {"accepted": payload["tenant_id"]}},
        compatible_sdk_ids=("sdk-python",),
    )
    registry.register_plugin(
        "plugin-faulty",
        name="Faulty Plugin",
        version="1.0.0",
        extension_points=("audit.export",),
        hooks={
            "before-export": lambda payload: (_ for _ in ()).throw(
                RuntimeError(f"boom for {payload['tenant_id']}")
            )
        },
        compatible_sdk_ids=("sdk-python",),
    )

    result = registry.run_hook(
        "plugin-audit-export", "before-export", {"tenant_id": "tenant-a"}
    )
    assert result == {"accepted": "tenant-a"}

    try:
        registry.run_hook("plugin-faulty", "before-export", {"tenant_id": "tenant-a"})
    except RuntimeError as exc:
        assert "isolated execution" in str(exc)
    else:  # pragma: no cover - fail closed if faulty plugins stop raising.
        raise AssertionError("faulty plugin unexpectedly succeeded")

    assert not registry.plugins["plugin-faulty"].enabled
    assert registry.summary()["event_count"] == 2
