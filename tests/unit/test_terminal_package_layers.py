from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.validate_layer_boundaries import (
    NON_PRODUCTION_LAYERS,
    discover_packages,
    validate,
)

def test_test_and_example_packages_have_terminal_layer_ownership() -> None:
    packages = {package.distribution: package for package in discover_packages(ROOT)}

    assert packages["tigrbl-identity-testkit"].layer == "100-tests"
    assert packages["acme-notes-cli"].layer == "105-examples"
    assert NON_PRODUCTION_LAYERS == {"100-tests", "105-examples"}


def test_production_packages_do_not_depend_on_terminal_packages() -> None:
    packages = discover_packages(ROOT)
    by_name = {package.distribution: package for package in packages}
    offenders: list[tuple[str, str]] = []

    for package in packages:
        if package.layer in NON_PRODUCTION_LAYERS:
            continue
        for dependency in package.dependencies:
            target = by_name.get(dependency)
            if target is not None and target.layer in NON_PRODUCTION_LAYERS:
                offenders.append((package.distribution, target.distribution))

    assert offenders == []


def test_examples_do_not_depend_on_test_packages() -> None:
    packages = discover_packages(ROOT)
    by_name = {package.distribution: package for package in packages}
    offenders = [
        (package.distribution, dependency)
        for package in packages
        if package.layer == "105-examples"
        for dependency in package.dependencies
        if dependency in by_name and by_name[dependency].layer == "100-tests"
    ]

    assert offenders == []


def test_terminal_layer_boundary_validator_is_clean() -> None:
    terminal_violations = [
        violation
        for violation in validate(ROOT)
        if violation.kind.startswith("terminal-layer-")
    ]

    assert terminal_violations == []
