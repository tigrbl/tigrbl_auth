from __future__ import annotations

import ast
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
LAYER = ROOT / "pkgs" / "30-storage-runtime"
TAXONOMY = yaml.safe_load(
    (ROOT / "architecture" / "durability-package-taxonomy.yaml").read_text(
        encoding="utf-8"
    )
)


def _imports(source: Path) -> set[str]:
    tree = ast.parse(source.read_text(encoding="utf-8"), filename=str(source))
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module)
    return imports


def test_every_layer_30_package_has_one_explicit_disposition() -> None:
    actual = {
        path.name for path in LAYER.iterdir() if (path / "pyproject.toml").exists()
    }
    declared = {
        TAXONOMY["substrate"],
        *TAXONOMY["canonical_packages"],
        *TAXONOMY["compatibility_packages"],
    }
    assert actual == declared


def test_canonical_durability_packages_have_no_higher_layer_imports() -> None:
    forbidden = (
        "tigrbl_auth_router_",
        "tigrbl_auth_protocol_",
        "tigrbl_authz_resource_server",
        "tigrbl_identity_runtime",
        "tigrbl_identity_server",
        "tigrbl_identity_storage_runtime",
    )
    packages = [TAXONOMY["substrate"], *TAXONOMY["canonical_packages"]]
    violations: list[str] = []
    for package in packages:
        for source in (LAYER / package).rglob("*.py"):
            for imported in _imports(source):
                if imported.startswith(forbidden):
                    violations.append(f"{source.relative_to(ROOT)} -> {imported}")
    assert violations == []


def test_canonical_durability_packages_do_not_define_repository_wrappers() -> None:
    forbidden_suffixes = ("Repository", "Store", "UnitOfWork", "Service")
    packages = [TAXONOMY["substrate"], *TAXONOMY["canonical_packages"]]
    violations: list[str] = []
    for package in packages:
        for source in (LAYER / package).rglob("*.py"):
            tree = ast.parse(source.read_text(encoding="utf-8"), filename=str(source))
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef) and node.name.endswith(
                    forbidden_suffixes
                ):
                    violations.append(f"{source.relative_to(ROOT)}:{node.lineno}")
    assert violations == []


def test_legacy_operation_and_spec_paths_are_identity_preserving_facades() -> None:
    from tigrbl_identity_storage_runtime.ops.webauthn_ceremonies import (
        consume_ceremony as legacy_consume,
    )
    from tigrbl_identity_storage_runtime.tables.webauthn import (
        WebAuthnCeremonyRuntimeSpec as legacy_spec,
    )
    from tigrbl_webauthn_durability.operations.webauthn_ceremonies import (
        consume_ceremony,
    )
    from tigrbl_webauthn_durability.specifications.webauthn import (
        WebAuthnCeremonyRuntimeSpec,
    )

    assert legacy_consume is consume_ceremony
    assert legacy_spec is WebAuthnCeremonyRuntimeSpec
    assert any(operation.alias == "consume_ceremony" for operation in legacy_spec.ops)


def test_engine_construction_is_owned_by_layer_30() -> None:
    canonical = (
        LAYER
        / "tigrbl-identity-storage-runtime/src/tigrbl_identity_storage_runtime/engine.py"
    ).read_text(encoding="utf-8")
    compatibility = (
        ROOT
        / "pkgs/60-runtime/tigrbl-identity-runtime/src/tigrbl_identity_runtime/engine.py"
    ).read_text(encoding="utf-8")
    assert "build_engine(" in canonical
    assert "tigrbl_identity_storage_runtime.engine" in compatibility
    assert "build_engine(" not in compatibility
