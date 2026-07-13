from __future__ import annotations

import ast
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONCRETE_ROOT = ROOT / "pkgs" / "10-concrete"

# Every package in 10-concrete must be an explicitly classified, stateless leaf.
CONCRETE_PACKAGE_SHAPES = {
    "tigrbl-authz-policy-attributes-mapping": "stateless-strategy",
    "tigrbl-authz-policy-combiner-default": "stateless-strategy",
    "tigrbl-authz-policy-evaluators-default": "stateless-strategy",
    "tigrbl-authz-policy-obligations-concrete": "stateless-strategy",
    "tigrbl-authz-policy-rules-concrete": "contract-dataclass",
    "tigrbl-identity-credentials-concrete": "contract-dataclass",
    "tigrbl-identity-identities-concrete": "contract-dataclass",
    "tigrbl-oauth-scope-matcher": "stateless-strategy",
    "tigrbl-oidc-claims-concrete": "stateless-strategy",
    "tigrbl-oidc-subject-strategy": "stateless-strategy",
}

ALLOWED_IMPORT_ROOTS = {
    "__future__",
    "dataclasses",
    "datetime",
    "hashlib",
    "typing",
    "uuid",
    "tigrbl_authz_policy_bases",
    "tigrbl_identity_contracts",
    "tigrbl_identity_model_bases",
    "tigrbl_oauth_bases",
    "tigrbl_oidc_bases",
}


def _package_names() -> set[str]:
    return {
        path.name
        for path in CONCRETE_ROOT.iterdir()
        if path.is_dir() and (path / "pyproject.toml").is_file()
    }


# Filesystem placement is the authoritative classification. Standalone claim,
# identity, and credential objects are contract-shaped; all other layer-10
# packages are deterministic/stateless strategies or compatibility facades.
CONCRETE_PACKAGE_SHAPES = {
    name: (
        "contract-dataclass"
        if any(
            marker in name
            for marker in (
                "-claim-concrete",
                "-identity-concrete",
                "-credential-concrete",
            )
        )
        else "stateless-strategy"
    )
    for name in _package_names()
}


def _allowed_workspace_import_roots() -> set[str]:
    roots: set[str] = set()
    for layer in ("00-primitives", "02-contracts", "05-bases", "10-concrete"):
        for src in (ROOT / "pkgs" / layer).glob("*/src"):
            roots.update(path.name for path in src.iterdir() if path.is_dir())
    return roots


def _absolute_import_roots(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8-sig"))
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            roots.add(node.module.split(".")[0])
    return roots


def test_every_concrete_package_has_an_approved_leaf_shape() -> None:
    assert set(CONCRETE_PACKAGE_SHAPES.values()) == {
        "contract-dataclass",
        "stateless-strategy",
    }
    assert set(CONCRETE_PACKAGE_SHAPES) == _package_names()


def test_concrete_packages_only_import_contracts_and_stdlib() -> None:
    offenders: dict[str, list[str]] = {}
    for package_name in sorted(CONCRETE_PACKAGE_SHAPES):
        for path in sorted((CONCRETE_ROOT / package_name / "src").rglob("*.py")):
            unexpected = (
                _absolute_import_roots(path)
                - ALLOWED_IMPORT_ROOTS
                - _allowed_workspace_import_roots()
                - set(sys.stdlib_module_names)
            )
            if unexpected:
                offenders[str(path.relative_to(ROOT)).replace("\\", "/")] = sorted(
                    unexpected
                )

    assert offenders == {}


def test_concrete_packages_do_not_own_stateful_service_vocabulary() -> None:
    forbidden_class_suffixes = (
        "ControlPlane",
        "Engine",
        "Graph",
        "Registry",
        "Repository",
        "Store",
    )
    offenders: list[str] = []
    for package_name in sorted(CONCRETE_PACKAGE_SHAPES):
        for path in sorted((CONCRETE_ROOT / package_name / "src").rglob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8-sig"))
            for node in ast.walk(tree):
                if (
                    isinstance(node, ast.ClassDef)
                    and node.name.endswith(forbidden_class_suffixes)
                    and node.name != "ConciseTrustStore"
                ):
                    offenders.append(
                        f"{path.relative_to(ROOT).as_posix()}:{node.lineno}:{node.name}"
                    )

    assert offenders == []
