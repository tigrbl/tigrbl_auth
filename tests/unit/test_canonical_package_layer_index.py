from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.package_layer_policy import dependency_allowed, load_layer_policy
from scripts.validate_layer_boundaries import LAYER_ORDER, discover_packages


EXPECTED_LAYER_ORDER = (
    "00-primitives",
    "01-storage",
    "02-contracts",
    "05-bases",
    "10-concrete",
    "20-providers",
    "30-storage-runtime",
    "40-capabilities",
    "50-protocols",
    "60-runtime",
    "70-facade",
    "80-routers",
    "90-backend-apps",
    "100-uix-core",
    "105-ui",
    "110-examples",
    "120-tests",
    "deprecated",
)


def test_canonical_package_layer_index_is_exact() -> None:
    policy = load_layer_policy(ROOT / "pkgs" / "layers.toml")

    assert policy.layer_ids == EXPECTED_LAYER_ORDER
    assert LAYER_ORDER == EXPECTED_LAYER_ORDER
    assert policy.terminal_layers == {"110-examples", "120-tests"}


def test_every_python_distribution_has_one_recognized_layer() -> None:
    packages = discover_packages(ROOT)
    distributions = [package.distribution for package in packages]

    assert len(distributions) == len(set(distributions))
    assert all(package.layer in EXPECTED_LAYER_ORDER for package in packages)


def test_terminal_dependency_policy_is_directional() -> None:
    policy = load_layer_policy(ROOT / "pkgs" / "layers.toml")

    assert dependency_allowed("110-examples", "70-facade", policy)
    assert dependency_allowed("120-tests", "70-facade", policy)
    assert dependency_allowed("120-tests", "110-examples", policy)
    assert not dependency_allowed("70-facade", "110-examples", policy)
    assert not dependency_allowed("70-facade", "120-tests", policy)
    assert not dependency_allowed("110-examples", "120-tests", policy)


def test_duplicate_layer_ids_are_rejected(tmp_path: Path) -> None:
    policy_path = tmp_path / "layers.toml"
    policy_path.write_text(
        """schema_version = 1
[[layers]]
id = \"10-concrete\"
order = 10
category = \"production\"
[[layers]]
id = \"10-concrete\"
order = 20
category = \"production\"
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="ids must be unique"):
        load_layer_policy(policy_path)
