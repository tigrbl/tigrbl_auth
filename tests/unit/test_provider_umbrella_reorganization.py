"""Boundary checks for provider umbrella compatibility migrations."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def test_provider_taxonomy_names_canonical_destinations() -> None:
    taxonomy = yaml.safe_load(
        (ROOT / "architecture" / "provider-package-taxonomy.yaml").read_text(
            encoding="utf-8"
        )
    )
    migrations = taxonomy["compatibility_or_migration_packages"]

    assert migrations["tigrbl-authn-credentials"] == {
        "target": "tba-credentials",
        "target_layer": "70-facade",
    }
    assert migrations["tba-provider-security-cose"]["target"] == (
        "tba-concrete-cose-plus-tba-provider-cose-cryptography"
    )


def test_compatibility_packages_reexport_canonical_objects() -> None:
    from tba_router_admin_gate import AdminGate as CanonicalAdminGate
    from tba_runtime_authorization_policy_admin_gate import AdminGate as LegacyAdminGate
    from tba_concrete_cose import decode_cose_key as canonical_decode
    from tba_credentials.lifecycle import hash_secret as canonical_hash
    from tba_authn_credentials.lifecycle import hash_secret as authn_legacy_hash
    from tba_provider_security_cose import decode_cose_key as legacy_decode
    from tigrbl_principal_authentication.lifecycle import hash_secret as legacy_hash

    assert LegacyAdminGate is CanonicalAdminGate
    assert legacy_decode is canonical_decode
    assert authn_legacy_hash is canonical_hash
    assert legacy_hash is canonical_hash


def test_credentials_facade_covers_each_credential_domain() -> None:
    import tba_credentials as credentials

    assert credentials.CredentialKind.PASSWORD.value == "password"
    assert credentials.digital.DigitalCredential is not None
    assert credentials.workload.WorkloadCredential is not None


def test_new_layer20_packages_do_not_import_downstream_layers() -> None:
    roots = (
        ROOT / "pkgs" / "20-providers" / "tba-provider-cose-cryptography",
        ROOT / "pkgs" / "20-providers" / "tba-provider-jose-swarmauri",
    )
    forbidden = (
        "tba_storage_core",
        "tba_runtime_identity_storage",
        "tba_runtime_identity",
        "tba_server_identity",
        "tba_protocol_",
        "tba_router_",
    )
    for root in roots:
        source = "\n".join(
            path.read_text(encoding="utf-8") for path in root.rglob("*.py")
        )
        assert not any(name in source for name in forbidden), root.name


def test_extracted_capability_families_bind_reportable_operations() -> None:
    import asyncio

    from tba_capability_access_governance import AccessGovernanceCapability
    from tigrbl_advanced_authentication_capability import (
        AdvancedAuthenticationCapability,
    )
    from tba_capability_key_administration import KeyAdministrationCapability
    from tba_capability_policy_administration import (
        PolicyAdministrationCapability,
    )
    from tba_capability_policy_assurance import PolicyAssuranceCapability

    capabilities = (
        (AccessGovernanceCapability(lambda value: value), "manage_entitlements"),
        (AdvancedAuthenticationCapability(lambda value: value), "begin"),
        (KeyAdministrationCapability(lambda value: value), "rotate"),
        (PolicyAdministrationCapability(lambda value: value), "administer"),
        (PolicyAssuranceCapability(lambda value: value), "evaluate"),
    )
    for capability, operation in capabilities:
        assert asyncio.run(capability.call(operation, "ok")).value == "ok"
        assert operation in capability.capability_report()["bound_operations"]
