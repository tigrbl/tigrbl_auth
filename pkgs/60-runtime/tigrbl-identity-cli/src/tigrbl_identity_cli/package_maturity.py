from __future__ import annotations

"""Package maturity evaluation for the split identity package suite."""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10 fallback
    import tomli as tomllib


SUPPORTED_PYTHON_VERSIONS = ("3.10", "3.11", "3.12", "3.13", "3.14")
PACKAGE_MATURITY_BOUNDARY_ID = "bnd:package-maturity-governance-slice"
PACKAGE_MATURITY_FEATURE_PREFIX = "feat:package-maturity-"
PACKAGE_MATURITY_FEATURE_ALIASES = {
    "tigrbl-auth-protocol-oauth": "oauth",
    "tigrbl-auth-protocol-oidc": "oidc",
    "tigrbl-auth-protocol-rp": "rp",
    "tigrbl-authn-credentials": "credentials",
    "tigrbl-authz-policy": "policy",
    "tigrbl-authz-resource-server": "resource-server",
    "tigrbl-auth": "facade",
    "tigrbl-identity-cli": "cli",
}


@dataclass(frozen=True, slots=True)
class PackageManifest:
    name: str
    version: str
    path: str
    import_root: str
    source_file_count: int
    readme_present: bool

    @property
    def maturity_feature_id(self) -> str:
        token = PACKAGE_MATURITY_FEATURE_ALIASES.get(
            self.name, self.name.removeprefix("tigrbl-identity-")
        )
        return f"{PACKAGE_MATURITY_FEATURE_PREFIX}{token}"

    def as_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "path": self.path,
            "import_root": self.import_root,
            "source_file_count": self.source_file_count,
            "readme_present": self.readme_present,
            "maturity_feature_id": self.maturity_feature_id,
        }


def _load_toml(path: Path) -> dict[str, Any]:
    return tomllib.loads(path.read_text(encoding="utf-8"))


def _import_root(package_root: Path, metadata: Mapping[str, Any], dist_name: str) -> str:
    poetry = metadata.get("tool", {}).get("poetry", {}) if isinstance(metadata, Mapping) else {}
    packages = poetry.get("packages", []) if isinstance(poetry, Mapping) else []
    if packages and isinstance(packages[0], Mapping) and packages[0].get("include"):
        return str(packages[0]["include"])
    src = package_root / "src"
    roots = sorted(item.name for item in src.iterdir() if item.is_dir()) if src.exists() else []
    return roots[0] if roots else dist_name.replace("-", "_")


def discover_package_manifests(repo_root: Path) -> list[PackageManifest]:
    root = repo_root.resolve()
    manifests: list[PackageManifest] = []
    for pyproject in sorted((root / "pkgs").glob("*/*/pyproject.toml")):
        if pyproject.parent.parent.name == "deprecated":
            continue
        metadata = _load_toml(pyproject)
        project = metadata.get("project", {})
        name = str(project.get("name") or "").strip()
        version = str(project.get("version") or "").strip()
        if not name or not version:
            raise ValueError(f"missing project.name or project.version in {pyproject}")
        package_root = pyproject.parent
        import_root = _import_root(package_root, metadata, name)
        src_root = package_root / "src" / import_root
        source_files = [path for path in src_root.rglob("*.py")] if src_root.exists() else []
        manifests.append(
            PackageManifest(
                name=name,
                version=version,
                path=package_root.relative_to(root).as_posix(),
                import_root=import_root,
                source_file_count=len(source_files),
                readme_present=(package_root / "README.md").exists(),
            )
        )
    return manifests


def build_package_python_matrix(
    packages: Iterable[PackageManifest],
    python_versions: Iterable[str] = SUPPORTED_PYTHON_VERSIONS,
) -> list[dict[str, str]]:
    cells: list[dict[str, str]] = []
    for package in packages:
        for python_version in python_versions:
            python_tag = f"py{python_version.replace('.', '')}"
            cross_cutting = package.name == "tigrbl-identity-testkit"
            test_paths = [
                f"tests/packages/{package.name}",
                f"tests/packages/{package.import_root}",
            ]
            if cross_cutting:
                test_paths.append("tests/interop")
            cells.append(
                {
                    "name": package.name,
                    "version": package.version,
                    "path": package.path,
                    "import_root": package.import_root,
                    "python_version": python_version,
                    "python_tag": python_tag,
                    "cell_id": f"{package.name}-{python_tag}",
                    "workspace_source_globs": "pkgs/*/*/src",
                    "package_test_paths": "\n".join(test_paths),
                    "cross_cutting": str(cross_cutting).lower(),
                }
            )
    return cells


def load_ssot_registry(repo_root: Path) -> dict[str, Any]:
    return json.loads((repo_root.resolve() / ".ssot" / "registry.json").read_text(encoding="utf-8"))


def _by_id(items: Iterable[Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    return {str(item.get("id")): item for item in items}


def evaluate_package_maturity(repo_root: Path, *, target_tier: str = "T2") -> dict[str, Any]:
    root = repo_root.resolve()
    registry = load_ssot_registry(root)
    packages = discover_package_manifests(root)
    feature_by_id = _by_id(registry.get("features", []))
    claim_by_id = _by_id(registry.get("claims", []))
    test_by_id = _by_id(registry.get("tests", []))
    boundary = _by_id(registry.get("boundaries", [])).get(PACKAGE_MATURITY_BOUNDARY_ID, {})
    boundary_feature_ids = set(boundary.get("feature_ids", []))
    matrix = build_package_python_matrix(packages)
    expected_cells = len(packages) * len(SUPPORTED_PYTHON_VERSIONS)

    failures: list[str] = []
    package_rows: list[dict[str, Any]] = []
    for package in packages:
        feature_id = package.maturity_feature_id
        feature = feature_by_id.get(feature_id)
        package_failures: list[str] = []
        if package.source_file_count <= 0:
            package_failures.append("missing package source files")
        if not package.readme_present:
            package_failures.append("missing README.md")
        if feature is None:
            package_failures.append(f"missing maturity feature {feature_id}")
        elif feature_id not in boundary_feature_ids:
            package_failures.append(f"maturity feature {feature_id} is outside boundary")
        elif feature.get("implementation_status") != "implemented":
            package_failures.append(f"maturity feature {feature_id} is not implemented")
        package_matrix_cells = [cell for cell in matrix if cell["name"] == package.name]
        if len(package_matrix_cells) != len(SUPPORTED_PYTHON_VERSIONS):
            package_failures.append("missing Python version matrix cells")
        tier = "T2" if not package_failures else "T1" if package.source_file_count > 0 else "T0"
        package_rows.append({**package.as_dict(), "tier": tier, "failures": package_failures})
        failures.extend(f"{package.name}: {item}" for item in package_failures)

    required_feature_ids = set(boundary_feature_ids)
    implemented_feature_ids = {
        feature_id
        for feature_id in required_feature_ids
        if feature_by_id.get(feature_id, {}).get("implementation_status") == "implemented"
    }
    missing_implemented = sorted(required_feature_ids - implemented_feature_ids)
    if missing_implemented:
        failures.append("boundary contains non-implemented features: " + ", ".join(missing_implemented))

    if len(matrix) != expected_cells:
        failures.append(f"expected {expected_cells} matrix cells, found {len(matrix)}")

    required_tiers = {"T0", "T1", "T2"}
    linked_claim_tiers: dict[str, set[str]] = {}
    linked_test_tiers: dict[str, set[str]] = {}
    for feature_id in required_feature_ids:
        feature = feature_by_id.get(feature_id, {})
        claim_tiers = {
            str(claim_by_id.get(claim_id, {}).get("tier"))
            for claim_id in feature.get("claim_ids", [])
            if claim_id in claim_by_id
        }
        test_tiers = {
            str(claim_by_id.get(claim_id, {}).get("tier"))
            for test_id in feature.get("test_ids", [])
            for claim_id in test_by_id.get(test_id, {}).get("claim_ids", [])
            if claim_id in claim_by_id
        }
        linked_claim_tiers[feature_id] = claim_tiers
        linked_test_tiers[feature_id] = test_tiers
        supported_tiers = claim_tiers | test_tiers
        if not required_tiers <= supported_tiers:
            failures.append(f"{feature_id} missing T0/T1/T2 claims")
        if not required_tiers <= test_tiers:
            failures.append(f"{feature_id} missing T0/T1/T2 tests")

    tier_order = {"T0": 0, "T1": 1, "T2": 2}
    target_index = tier_order.get(target_tier, 2)
    achieved_index = 2 if not failures else min(tier_order[row["tier"]] for row in package_rows) if package_rows else 0
    passed = not failures and achieved_index >= target_index
    return {
        "passed": passed,
        "target_tier": target_tier,
        "achieved_tier": next(key for key, value in tier_order.items() if value == achieved_index),
        "failures": failures,
        "warnings": [],
        "summary": {
            "package_count": len(packages),
            "boundary_feature_count": len(required_feature_ids),
            "implemented_boundary_feature_count": len(implemented_feature_ids),
            "python_version_count": len(SUPPORTED_PYTHON_VERSIONS),
            "matrix_cell_count": len(matrix),
            "expected_matrix_cell_count": expected_cells,
        },
        "packages": package_rows,
        "matrix": matrix,
        "claim_tiers": {key: sorted(value) for key, value in linked_claim_tiers.items()},
        "test_tiers": {key: sorted(value) for key, value in linked_test_tiers.items()},
    }


def run_package_maturity_gate(repo_root: Path, *, target_tier: str = "T2") -> int:
    return 0 if evaluate_package_maturity(repo_root, target_tier=target_tier)["passed"] else 1


__all__ = [
    "PACKAGE_MATURITY_BOUNDARY_ID",
    "SUPPORTED_PYTHON_VERSIONS",
    "PackageManifest",
    "build_package_python_matrix",
    "discover_package_manifests",
    "evaluate_package_maturity",
    "run_package_maturity_gate",
]
