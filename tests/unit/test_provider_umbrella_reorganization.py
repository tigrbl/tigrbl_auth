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

    assert migrations["tigrbl-authn-credentials"]["target"] == (
        "tigrbl-principal-authentication"
    )
    assert migrations["tigrbl-authz-policy-admin-gate"]["target"] == (
        "tigrbl-auth-api-admin-gate"
    )
    assert migrations["tigrbl-authz-policy-decision-engine"]["target"] == (
        "tigrbl-policy-decision-engine-default"
    )
    assert migrations["tigrbl-security-cose"]["target"] == (
        "tigrbl-cose-concrete-plus-tigrbl-cose-cryptography-provider"
    )


def test_compatibility_packages_reexport_canonical_objects() -> None:
    from tigrbl_auth_api_admin_gate import AdminGate as CanonicalAdminGate
    from tigrbl_authz_policy_admin_gate import AdminGate as LegacyAdminGate
    from tigrbl_cose_concrete import decode_cose_key as canonical_decode
    from tigrbl_principal_authentication.lifecycle import hash_secret as canonical_hash
    from tigrbl_security_cose import decode_cose_key as legacy_decode
    from tigrbl_authn_credentials.lifecycle import hash_secret as legacy_hash

    assert LegacyAdminGate is CanonicalAdminGate
    assert legacy_decode is canonical_decode
    assert legacy_hash is canonical_hash


def test_new_layer20_packages_do_not_import_downstream_layers() -> None:
    roots = (
        ROOT / "pkgs" / "20-providers" / "tigrbl-cose-cryptography-provider",
        ROOT / "pkgs" / "20-providers" / "tigrbl-jose-swarmauri-provider",
    )
    forbidden = (
        "tigrbl_identity_storage",
        "tigrbl_identity_storage_runtime",
        "tigrbl_identity_runtime",
        "tigrbl_identity_server",
        "tigrbl_auth_protocol_",
        "tigrbl_auth_api_",
    )
    for root in roots:
        source = "\n".join(
            path.read_text(encoding="utf-8") for path in root.rglob("*.py")
        )
        assert not any(name in source for name in forbidden), root.name


def test_extracted_capability_families_bind_reportable_operations() -> None:
    import asyncio

    from tigrbl_access_governance_capability import AccessGovernanceCapability
    from tigrbl_advanced_authentication_capability import (
        AdvancedAuthenticationCapability,
    )
    from tigrbl_key_administration_capability import KeyAdministrationCapability
    from tigrbl_policy_administration_capability import (
        PolicyAdministrationCapability,
    )
    from tigrbl_policy_assurance_capability import PolicyAssuranceCapability

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
