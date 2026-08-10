from __future__ import annotations

import ast
from importlib import import_module
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
TAXONOMY = ROOT / "architecture" / "contract-package-taxonomy.yaml"
CONTRACTS = ROOT / "pkgs" / "02-contracts"
CANONICAL_MIGRATED_PACKAGES = (
    "tigrbl-administration-contracts",
    "tigrbl-authorization-contracts",
    "tigrbl-audit-contracts",
    "tigrbl-delegation-contracts",
    "tigrbl-governance-contracts",
)


def test_active_contract_taxonomy_names_live_packages() -> None:
    document = yaml.safe_load(TAXONOMY.read_text(encoding="utf-8"))
    assert document["version"] == 1
    assert document["layer"] == "02-contracts"

    active = {
        package
        for group, families in document["families"].items()
        if group != "pending_extraction"
        for package in families.values()
    }
    for package in active:
        assert (CONTRACTS / package / "pyproject.toml").is_file(), package


def test_compatibility_facades_preserve_canonical_object_identity() -> None:
    pairs = (
        ("tigrbl_claim_contracts", "tigrbl_identity_contracts.claims", "Claim"),
        ("tigrbl_did_contracts", "tigrbl_identity_contracts.did", "Did"),
        (
            "tigrbl_digital_credential_contracts",
            "tigrbl_identity_contracts.digital_credentials",
            "DigitalCredential",
        ),
        (
            "tigrbl_public_key_authentication_contracts",
            "tigrbl_identity_contracts.public_key_authentication",
            "PublicKeyCredentialSource",
        ),
        (
            "tigrbl_replay_contracts",
            "tigrbl_identity_contracts.replay.reservations",
            "ReplayReservationPort",
        ),
        (
            "tigrbl_security_event_contracts",
            "tigrbl_identity_contracts.security_events",
            "SecurityEvent",
        ),
        (
            "tigrbl_workload_identity_contracts",
            "tigrbl_identity_contracts.workloads",
            "Svid",
        ),
        (
            "tigrbl_attestation_contracts",
            "tigrbl_identity_contracts.attestation",
            "AttestationEvidence",
        ),
        (
            "tigrbl_administration_contracts",
            "tigrbl_identity_contracts",
            "PlatformAdministrator",
        ),
        (
            "tigrbl_authorization_contracts",
            "tigrbl_identity_contracts",
            "ScopeMatchRequest",
        ),
        (
            "tigrbl_audit_contracts",
            "tigrbl_identity_contracts",
            "AdminAuditEvent",
        ),
        (
            "tigrbl_delegation_contracts",
            "tigrbl_identity_contracts",
            "DelegatedAdminScope",
        ),
        (
            "tigrbl_governance_contracts",
            "tigrbl_identity_contracts",
            "AccessReviewItem",
        ),
    )
    for canonical_module, compatibility_module, name in pairs:
        canonical = getattr(import_module(canonical_module), name)
        compatibility = getattr(import_module(compatibility_module), name)
        assert compatibility is canonical, (compatibility_module, name)


def test_extracted_compatibility_modules_define_no_classes() -> None:
    roots = (
        "claims",
        "did",
        "digital_credentials",
        "public_key_authentication",
        "security_events",
        "workloads",
    )
    identity = (
        CONTRACTS
        / "tigrbl-identity-contracts"
        / "src"
        / "tigrbl_identity_contracts"
    )
    for root in roots:
        for path in (identity / root).rglob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            assert not any(isinstance(node, ast.ClassDef) for node in ast.walk(tree)), path


def test_canonical_contract_packages_do_not_import_compatibility_aggregate() -> None:
    packages = (
        "tigrbl-attestation-contracts",
        "tigrbl-claim-contracts",
        "tigrbl-did-contracts",
        "tigrbl-digital-credential-contracts",
        "tigrbl-public-key-authentication-contracts",
        "tigrbl-replay-contracts",
        "tigrbl-security-event-contracts",
        "tigrbl-workload-identity-contracts",
        *CANONICAL_MIGRATED_PACKAGES,
    )
    for package in packages:
        for path in (CONTRACTS / package / "src").rglob("*.py"):
            assert "tigrbl_identity_contracts" not in path.read_text(encoding="utf-8"), path


def test_identity_contract_shims_export_canonical_objects_for_migrated_families() -> None:
    identity_contracts = import_module("tigrbl_identity_contracts")
    canonical_exports = (
        ("tigrbl_administration_contracts", "PlatformAdministrator"),
        ("tigrbl_authorization_contracts", "ScopeMatchRequest"),
        ("tigrbl_audit_contracts", "AdminAuditEvent"),
        ("tigrbl_delegation_contracts", "DelegatedAdminScope"),
        ("tigrbl_governance_contracts", "AccessReviewItem"),
    )
    for canonical_package, symbol in canonical_exports:
        canonical = getattr(import_module(canonical_package), symbol)
        compatibility = getattr(identity_contracts, symbol)
        assert compatibility is canonical, (canonical_package, symbol)
