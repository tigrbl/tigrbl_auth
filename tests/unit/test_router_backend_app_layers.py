from __future__ import annotations

import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.validate_layer_boundaries import discover_packages, validate  # noqa: E402


def test_router_and_backend_app_families_are_explicit() -> None:
    packages = discover_packages(ROOT)
    routers = [package for package in packages if package.layer == "80-routers"]
    apps = [package for package in packages if package.layer == "90-backend-apps"]

    assert len(routers) == 17
    assert len(apps) == 7
    assert all(
        package.distribution.startswith("tigrbl-auth-router-") for package in routers
    )
    assert all(
        package.distribution.startswith("tigrbl-auth-backend-app-") for package in apps
    )


def test_routers_do_not_depend_on_or_import_backend_apps() -> None:
    forbidden_kinds = {
        "router-depends-on-backend-app",
        "router-imports-backend-app",
    }
    violations = [
        violation for violation in validate(ROOT) if violation.kind in forbidden_kinds
    ]

    assert violations == []


def test_each_backend_app_closes_over_a_router_surface() -> None:
    packages = discover_packages(ROOT)
    distributions = {package.distribution: package for package in packages}
    apps = [package for package in packages if package.layer == "90-backend-apps"]

    for app in apps:
        router_dependencies = {
            dependency
            for dependency in app.dependencies
            if dependency in distributions
            and distributions[dependency].layer == "80-routers"
        }
        local_router = any(
            "TigrblRouter(" in source.read_text(encoding="utf-8-sig")
            for source in (app.path / "src").rglob("*.py")
        )
        assert router_dependencies or local_router, app.distribution


def test_backend_app_contracts_match_router_dependencies() -> None:
    packages = discover_packages(ROOT)
    distributions = {package.distribution: package for package in packages}
    apps = [package for package in packages if package.layer == "90-backend-apps"]

    for app in apps:
        assert len(app.import_roots) == 1, app.distribution
        module = importlib.import_module(app.import_roots[0])
        contract_names = [
            name for name in module.__all__ if name.endswith("_BACKEND_APP_CONTRACT")
        ]
        assert len(contract_names) == 1, app.distribution
        contract = getattr(module, contract_names[0])
        declared = set(contract.mounted_router_packages)
        dependencies = {
            dependency
            for dependency in app.dependencies
            if dependency in distributions
            and distributions[dependency].layer == "80-routers"
        }

        assert declared == dependencies, app.distribution
