from __future__ import annotations

import ast
import importlib
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
for src in sorted((ROOT / "pkgs").glob("*/*/src")):
    value = str(src)
    if value not in sys.path:
        sys.path.insert(0, value)


def test_release_contracts_export_release_assurance_dtos() -> None:
    import tba_contracts_release as contracts
    import tigrbl_identity_identities_concrete as identity_concrete
    from tba_certification_release.certification import AlgorithmPolicy, CertificationError
    from tba_certification_release.certification import MachineIdentity

    assert contracts.ReleaseAssuranceError is contracts.CertificationError
    assert CertificationError is contracts.CertificationError
    assert AlgorithmPolicy is contracts.AlgorithmPolicy
    assert not hasattr(contracts, "MachineIdentity")
    assert MachineIdentity is identity_concrete.MachineIdentity
    assert contracts.RuntimeQualification(
        artifact_sha256="a",
        dependency_lock_sha256="b",
        config_sha256="c",
        product_surface="public-app",
        capabilities=frozenset({"jwks"}),
    ).product_surface == "public-app"


def test_release_certification_modules_do_not_define_moved_contract_classes() -> None:
    certification_root = (
        ROOT
        / "pkgs"
        / "60-runtime"
        / "tba-certification-release"
        / "src"
        / "tba_certification_release"
        / "certification"
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


def test_authz_policy_no_longer_exposes_release_certification_or_posture_modules() -> None:
    authz_root = (
        ROOT
        / "pkgs"
        / "40-capabilities"
        / "tba-runtime-authorization-policy"
        / "src"
        / "tba_runtime_authorization_policy"
    )
    removed_paths = (
        authz_root / "certification.py",
        authz_root / "_certification",
        authz_root / "release_posture.py",
        authz_root / "_release_posture",
    )

    assert not any(path.exists() for path in removed_paths)

    for module_name in (
        "tba_runtime_authorization_policy.certification",
        "tba_runtime_authorization_policy._certification",
        "tba_runtime_authorization_policy.release_posture",
        "tba_runtime_authorization_policy._release_posture",
    ):
        sys.modules.pop(module_name, None)
        with pytest.raises(ModuleNotFoundError):
            importlib.import_module(module_name)


def test_release_contracts_do_not_import_runtime_or_capability_packages() -> None:
    contracts_root = (
        ROOT
        / "pkgs"
        / "02-contracts"
        / "tba-contracts-release"
        / "src"
        / "tba_contracts_release"
    )
    forbidden = {
        "tba_auth",
        "tba_runtime_authorization_policy",
        "tba_runtime_identity_authoring",
        "tba_cli_identity",
        "tba_storage_core",
        "tba_certification_release",
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
