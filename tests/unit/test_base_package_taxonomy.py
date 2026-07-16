from __future__ import annotations

import importlib
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
TAXONOMY = ROOT / "architecture" / "base-package-taxonomy.yaml"
BASES = ROOT / "pkgs" / "05-bases"


def _package_names(section: dict[str, str]) -> set[str]:
    return set(section.values())


def test_canonical_base_packages_exist_and_are_unique() -> None:
    data = yaml.safe_load(TAXONOMY.read_text(encoding="utf-8"))
    families = data["families"]
    declared: list[str] = []
    for section in families.values():
        declared.extend(section.values())
    assert len(declared) == len(set(declared))
    for package in declared:
        assert (BASES / package / "pyproject.toml").is_file(), package


def test_compatibility_aggregates_depend_on_canonical_owners() -> None:
    data = yaml.safe_load(TAXONOMY.read_text(encoding="utf-8"))
    for aggregate, spec in data["compatibility_aggregates"].items():
        canonical = spec["canonical"]
        owners = (canonical,) if isinstance(canonical, str) else tuple(canonical)
        metadata = (BASES / aggregate / "pyproject.toml").read_text(encoding="utf-8")
        for owner in owners:
            assert owner in metadata, (aggregate, owner)


def test_canonical_and_compatibility_exports_are_identical() -> None:
    pairs = {
        "tigrbl_identity_claims_bases": "tigrbl_claim_bases",
        "tigrbl_identity_authenticator_bases": "tigrbl_authenticator_bases",
        "tigrbl_public_key_authenticator_bases": "tigrbl_public_key_authentication_bases",
        "tigrbl_security_artifact_bases": "tigrbl_protected_artifact_bases",
    }
    for compatibility_name, canonical_name in pairs.items():
        compatibility = importlib.import_module(compatibility_name)
        canonical = importlib.import_module(canonical_name)
        for name in canonical.__all__:
            assert getattr(compatibility, name) is getattr(canonical, name)


def test_model_normalization_is_owned_by_layer_zero() -> None:
    compatibility = importlib.import_module("tigrbl_identity_model_bases")
    primitives = importlib.import_module("tigrbl_identity_core")
    for name in ("clean_mapping", "clean_tuple", "new_model_id", "required_text"):
        assert getattr(compatibility, name) is getattr(primitives, name)
