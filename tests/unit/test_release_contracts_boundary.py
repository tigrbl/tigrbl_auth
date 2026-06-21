from __future__ import annotations

import ast
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
for src in sorted((ROOT / "pkgs").glob("*/*/src")):
    value = str(src)
    if value not in sys.path:
        sys.path.insert(0, value)


def test_release_contracts_export_release_assurance_dtos() -> None:
    import tigrbl_release_contracts as contracts
    import tigrbl_identity_concrete as concrete
    from tigrbl_authz_policy._certification import AlgorithmPolicy, CertificationError
    from tigrbl_authz_policy._certification import MachineIdentity

    assert contracts.ReleaseAssuranceError is contracts.CertificationError
    assert CertificationError is contracts.CertificationError
    assert AlgorithmPolicy is contracts.AlgorithmPolicy
    assert not hasattr(contracts, "MachineIdentity")
    assert MachineIdentity is concrete.MachineIdentity
    assert contracts.RuntimeQualification(
        artifact_sha256="a",
        dependency_lock_sha256="b",
        config_sha256="c",
        product_surface="public-api",
        capabilities=frozenset({"jwks"}),
    ).product_surface == "public-api"


def test_authz_certification_modules_do_not_define_moved_contract_classes() -> None:
    certification_root = (
        ROOT
        / "pkgs"
        / "40-capabilities"
        / "tigrbl-authz-policy"
        / "src"
        / "tigrbl_authz_policy"
        / "_certification"
    )
    moved = {
        "AlgorithmPolicy",
        "AuthorizationEvent",
        "AuthorizationSnapshot",
        "AuthorizationState",
        "CapabilityRecord",
        "CertificationError",
        "DelegationStep",
        "KeyBoundary",
        "MachineIdentity",
        "RealmState",
        "RuntimeQualification",
        "TenantState",
        "VerifierPolicy",
    }

    for path in certification_root.glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        defined = {
            node.name
            for node in ast.walk(tree)
            if isinstance(node, ast.ClassDef) and node.name in moved
        }
        assert not defined, f"{path} still owns moved release contracts: {sorted(defined)}"


def test_release_contracts_do_not_import_runtime_or_capability_packages() -> None:
    contracts_root = (
        ROOT
        / "pkgs"
        / "01-contracts"
        / "tigrbl-release-contracts"
        / "src"
        / "tigrbl_release_contracts"
    )
    forbidden = {
        "tigrbl_auth",
        "tigrbl_authz_policy",
        "tigrbl_identity_author",
        "tigrbl_identity_cli",
        "tigrbl_identity_storage",
    }

    for path in contracts_root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imports: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split(".")[0])
        assert not (imports & forbidden), path
