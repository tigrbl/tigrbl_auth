from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
for src in sorted((ROOT / "pkgs").glob("*/src")):
    value = str(src)
    if value not in sys.path:
        sys.path.append(value)

from tigrbl_identity_operator.package_maturity import (  # noqa: E402
    PACKAGE_MATURITY_BOUNDARY_ID,
    SUPPORTED_PYTHON_VERSIONS,
    build_package_python_matrix,
    discover_package_manifests,
    evaluate_package_maturity,
    run_package_maturity_gate,
)


def test_package_maturity_t0_discovers_all_split_packages() -> None:
    packages = discover_package_manifests(ROOT)

    assert len(packages) >= 25
    assert {package.name for package in packages} >= {
        "tigrbl-auth",
        "tigrbl-identity-core",
        "tigrbl-identity-cli",
        "tigrbl-identity-operator",
        "tigrbl-identity-testkit",
    }
    assert all(package.version for package in packages)
    assert all(package.path.startswith("pkgs/") for package in packages)


def test_package_maturity_t1_maps_every_package_to_boundary_feature() -> None:
    report = evaluate_package_maturity(ROOT, target_tier="T1")
    feature_ids = {row["maturity_feature_id"] for row in report["packages"]}
    boundary_feature_ids = set(report["claim_tiers"])

    assert PACKAGE_MATURITY_BOUNDARY_ID == "bnd:package-maturity-governance-slice"
    assert "feat:package-maturity-facade" in feature_ids
    assert feature_ids <= boundary_feature_ids
    assert report["summary"]["package_count"] == len(discover_package_manifests(ROOT))


def test_package_maturity_t2_builds_complete_package_python_matrix() -> None:
    packages = discover_package_manifests(ROOT)
    matrix = build_package_python_matrix(packages)

    assert len(matrix) == len(packages) * len(SUPPORTED_PYTHON_VERSIONS)
    assert {
        cell["python_version"]
        for cell in matrix
        if cell["name"] == "tigrbl-identity-core"
    } == set(SUPPORTED_PYTHON_VERSIONS)
    testkit_cells = [cell for cell in matrix if cell["name"] == "tigrbl-identity-testkit"]
    assert len(testkit_cells) == len(SUPPORTED_PYTHON_VERSIONS)
    assert all(cell["cross_cutting"] == "true" for cell in testkit_cells)
    assert all("tests/packages/tigrbl-identity-testkit" in cell["package_test_paths"] for cell in testkit_cells)
    assert all("tests/integration" not in cell["package_test_paths"] for cell in testkit_cells)
    assert all("tests/interop" in cell["package_test_paths"] for cell in testkit_cells)


def test_package_maturity_t2_gate_passes_with_claim_test_links() -> None:
    report = evaluate_package_maturity(ROOT, target_tier="T2")

    assert report["passed"], report["failures"]
    assert report["achieved_tier"] == "T2"
    assert report["summary"]["boundary_feature_count"] >= 28
    assert report["summary"]["implemented_boundary_feature_count"] == report["summary"]["boundary_feature_count"]
    assert run_package_maturity_gate(ROOT, target_tier="T2") == 0
