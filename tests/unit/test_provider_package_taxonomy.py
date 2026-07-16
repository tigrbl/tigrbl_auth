from __future__ import annotations

from pathlib import Path

import tomllib
import yaml


ROOT = Path(__file__).resolve().parents[2]
PKGS = ROOT / "pkgs"
PROVIDERS = PKGS / "20-providers"
TAXONOMY = ROOT / "architecture" / "provider-package-taxonomy.yaml"
FORBIDDEN_LAYERS = {
    "01-storage",
    "30-storage-runtime",
    "40-capabilities",
    "50-protocols",
    "60-runtime",
    "70-facade",
    "80-apis",
}


def _data() -> dict[str, object]:
    return yaml.safe_load(TAXONOMY.read_text(encoding="utf-8"))


def _canonical(data: dict[str, object]) -> set[str]:
    families = data["canonical_providers"]
    return {package for packages in families.values() for package in packages}


def _package_layers() -> dict[str, str]:
    result: dict[str, str] = {}
    for metadata_path in PKGS.rglob("pyproject.toml"):
        metadata = tomllib.loads(metadata_path.read_text(encoding="utf-8-sig"))
        result[metadata["project"]["name"]] = metadata_path.relative_to(PKGS).parts[0]
    return result


def test_every_layer_20_package_has_exactly_one_disposition() -> None:
    data = _data()
    canonical = _canonical(data)
    migrating = set(data["compatibility_or_migration_packages"])
    discovered = {
        path.name
        for path in PROVIDERS.iterdir()
        if path.is_dir() and (path / "pyproject.toml").is_file()
    }
    assert canonical.isdisjoint(migrating)
    assert canonical | migrating == discovered


def test_canonical_providers_do_not_reverse_dependency_direction() -> None:
    data = _data()
    layers = _package_layers()
    violations: list[str] = []
    for package in sorted(_canonical(data)):
        metadata_path = PROVIDERS / package / "pyproject.toml"
        metadata = tomllib.loads(metadata_path.read_text(encoding="utf-8-sig"))
        for requirement in metadata["project"].get("dependencies", ()):
            dependency = (
                requirement.split("==", 1)[0].split(">=", 1)[0].split("[", 1)[0]
            )
            if layers.get(dependency) in FORBIDDEN_LAYERS:
                violations.append(f"{package} -> {dependency} ({layers[dependency]})")
    assert violations == []


def test_declared_deterministic_extractions_exist_in_layer_10() -> None:
    data = _data()
    for package in data["canonical_deterministic_extractions"]:
        assert (PKGS / "10-concrete" / package / "pyproject.toml").is_file(), package
