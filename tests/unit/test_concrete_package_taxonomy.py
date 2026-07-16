from __future__ import annotations

import ast
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
CONCRETE = ROOT / "pkgs" / "10-concrete"
TAXONOMY = ROOT / "architecture" / "concrete-package-taxonomy.yaml"


def _imports(path: Path) -> set[str]:
    roots: set[str] = set()
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            roots.add(node.module.split(".", 1)[0])
    return roots


def test_declared_canonical_concrete_packages_exist() -> None:
    data = yaml.safe_load(TAXONOMY.read_text(encoding="utf-8"))
    for spec in data["families"].values():
        for package in spec.get("packages", ()):
            assert (CONCRETE / package / "pyproject.toml").is_file(), package


def test_layer_10_never_imports_higher_layers() -> None:
    data = yaml.safe_load(TAXONOMY.read_text(encoding="utf-8"))
    forbidden_fragments = (
        "_provider",
        "_storage_runtime",
        "_capability",
        "_protocol_",
        "_runtime",
        "_api_",
    )
    exceptions = {"tigrbl_capability", "tigrbl_default_capability"} | {
        name.replace("-", "_") for name in data["compatibility_aggregates"]
    }
    for path in sorted(CONCRETE.rglob("*.py")):
        if "tests" in path.parts:
            continue
        package = next(part for part in path.parts if part.startswith("tigrbl-"))
        module = package.replace("-", "_")
        if module in exceptions:
            continue
        for imported in _imports(path):
            assert not any(part in imported for part in forbidden_fragments), (
                path,
                imported,
            )


def test_identity_and_authentication_credential_packages_use_canonical_bases() -> None:
    data = yaml.safe_load(TAXONOMY.read_text(encoding="utf-8"))
    for package in data["families"]["identity"]["packages"]:
        metadata = (CONCRETE / package / "pyproject.toml").read_text(encoding="utf-8")
        assert "tigrbl-identity-bases" in metadata, package
    credential_packages = sorted(CONCRETE.glob("tigrbl-*-credential-concrete"))
    digital = set(data["families"]["digital_credential"]["packages"])
    for package in credential_packages:
        metadata = (package / "pyproject.toml").read_text(encoding="utf-8")
        expected = (
            "tigrbl-digital-credential-bases"
            if package.name in digital
            else "tigrbl-authentication-credential-bases"
        )
        assert expected in metadata, package.name
