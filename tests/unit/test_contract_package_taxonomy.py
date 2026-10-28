from __future__ import annotations

import ast
from importlib import import_module
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
TAXONOMY = ROOT / "architecture" / "contract-package-taxonomy.yaml"
CONTRACTS = ROOT / "pkgs" / "02-contracts"
CANONICAL_MIGRATED_PACKAGES = (
    "tba-administration-contracts",
    "tba-contracts-authorization",
    "tba-audit-contracts",
    "tba-delegation-contracts",
    "tba-governance-contracts",
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
        ("tba_contracts_claim", "tba_contracts_identity.claims", "Claim"),
        ("tba_contracts_did", "tba_contracts_identity.did", "Did"),
        (
            "tba_contracts_digital_credential",
            "tba_contracts_identity.digital_credentials",
            "DigitalCredential",
        ),
        (
            "tba_contracts_public_key_authentication",
            "tba_contracts_identity.public_key_authentication",
            "PublicKeyCredentialSource",
        ),
        (
            "tba_contracts_replay",
            "tba_contracts_identity.replay.reservations",
            "ReplayReservationPort",
        ),
        (
            "tba_contracts_security_event",
            "tba_contracts_identity.security_events",
            "SecurityEvent",
        ),
        (
            "tba_contracts_workload_identity",
            "tba_contracts_identity.workloads",
            "Svid",
        ),
        (
            "tba_contracts_attestation",
            "tba_contracts_identity.attestation",
            "AttestationEvidence",
        ),
        (
            "tba_administration_contracts",
            "tba_contracts_identity",
            "PlatformAdministrator",
        ),
        (
            "tba_contracts_authorization",
            "tba_contracts_identity",
            "ScopeMatchRequest",
        ),
        (
            "tba_audit_contracts",
            "tba_contracts_identity",
            "AdminAuditEvent",
        ),
        (
            "tba_delegation_contracts",
            "tba_contracts_identity",
            "DelegatedAdminScope",
        ),
        (
            "tba_governance_contracts",
            "tba_contracts_identity",
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
        / "tba-contracts-identity"
        / "src"
        / "tba_contracts_identity"
    )
    for root in roots:
        for path in (identity / root).rglob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            assert not any(isinstance(node, ast.ClassDef) for node in ast.walk(tree)), path


def test_canonical_contract_packages_do_not_import_compatibility_aggregate() -> None:
    packages = (
        "tba-contracts-attestation",
        "tba-contracts-claim",
        "tba-contracts-did",
        "tba-contracts-digital-credential",
        "tba-contracts-public-key-authentication",
        "tba-contracts-replay",
        "tba-contracts-security-event",
        "tba-contracts-workload-identity",
        *CANONICAL_MIGRATED_PACKAGES,
    )
    for package in packages:
        for path in (CONTRACTS / package / "src").rglob("*.py"):
            assert "tba_contracts_identity" not in path.read_text(encoding="utf-8"), path


def test_identity_contract_shims_export_canonical_objects_for_migrated_families() -> None:
    identity_contracts = import_module("tba_contracts_identity")
    canonical_exports = (
        ("tba_administration_contracts", "PlatformAdministrator"),
        ("tba_contracts_authorization", "ScopeMatchRequest"),
        ("tba_audit_contracts", "AdminAuditEvent"),
        ("tba_delegation_contracts", "DelegatedAdminScope"),
        ("tba_governance_contracts", "AccessReviewItem"),
    )
    for canonical_package, symbol in canonical_exports:
        canonical = getattr(import_module(canonical_package), symbol)
        compatibility = getattr(identity_contracts, symbol)
        assert compatibility is canonical, (canonical_package, symbol)
