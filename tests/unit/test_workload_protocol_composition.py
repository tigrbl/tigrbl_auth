"""Enforce standalone workload protocol package dependency boundaries."""

from pathlib import Path

import pytest

try:
    import tomllib
except ModuleNotFoundError:  # Python 3.10
    import tomli as tomllib

from packaging.requirements import Requirement


PACKAGES = Path(__file__).resolve().parents[2] / "pkgs"


@pytest.fixture(scope="module")
def dependencies():
    projects = {}
    for manifest in PACKAGES.glob("*/*/pyproject.toml"):
        project = tomllib.loads(manifest.read_text(encoding="utf-8")).get("project")
        if project:
            projects[project["name"]] = {
                Requirement(requirement).name for requirement in project.get("dependencies", [])
            }
    return projects


@pytest.mark.parametrize(
    ("roots", "excluded"),
    [
        (
            (
                "tba-profile-workload-credential-wimse-wit",
                "tba-profile-workload-proof-wimse-wpt",
            ),
            ("spiffe", "spire"),
        ),
        (
            (
                "tba-protocol-workload-spiffe-svid",
                "tba-protocol-workload-spiffe-workload-api",
                "tba-provider-spiffe-bundle",
                "tba-provider-spiffe-workload-api",
            ),
            ("wimse", "spire"),
        ),
    ],
    ids=["standalone-wimse", "standalone-spiffe"],
)
def test_standalone_workload_protocol_dependency_closure(dependencies, roots, excluded):
    pending = list(roots)
    seen = set()
    assert set(roots) <= dependencies.keys()
    while pending:
        package = pending.pop()
        if package in seen:
            continue
        seen.add(package)
        pending.extend(dependencies.get(package, ()))

    forbidden = {
        package
        for package in seen
        if set(package.lower().replace("_", "-").split("-")).intersection(excluded)
    }
    assert not forbidden, f"Unexpected protocol dependencies: {sorted(forbidden)}"


def test_wit_svid_declares_both_protocol_dependencies(dependencies):
    assert {
        "tba-profile-workload-credential-wimse-wit",
        "tba-protocol-workload-spiffe-svid",
    } <= dependencies["tba-profile-workload-credential-spiffe-wit-svid"]
