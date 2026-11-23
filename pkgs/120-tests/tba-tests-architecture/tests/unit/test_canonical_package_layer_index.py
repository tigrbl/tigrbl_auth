from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[5]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.package_layer_policy import (
    DependencyRule,
    classify_layer,
    dependency_allowed,
    load_layer_policy,
    package_dependency_allowed,
)
from scripts.validate_layer_boundaries import LAYER_ORDER, discover_packages


EXPECTED_LAYER_ORDER = (
    "000-primitives",
    "001-storage",
    "002-contracts",
    "003-codecs",
    "005-bases",
    "010-concrete",
    "020-providers",
    "030-storage-runtime",
    "040-capabilities",
    "050-protocols",
    "055-profiles",
    "060-runtime",
    "070-facade",
    "075-clients",
    "080-routers",
    "085-middleware",
    "090-backend-apps",
    "100-uix-core",
    "105-ui",
    "106-ui",
    "110-examples",
    "120-tests",
    "deprecated",
)


def test_canonical_package_layer_index_is_exact() -> None:
    policy = load_layer_policy()

    assert policy.layer_ids == EXPECTED_LAYER_ORDER
    assert LAYER_ORDER == EXPECTED_LAYER_ORDER
    assert policy.terminal_layers == {"110-examples", "120-tests"}


def test_every_python_distribution_has_one_recognized_layer() -> None:
    packages = discover_packages(ROOT)
    distributions = [package.distribution for package in packages]

    assert len(distributions) == len(set(distributions))
    assert all(package.layer in EXPECTED_LAYER_ORDER for package in packages)


def test_terminal_dependency_policy_is_directional() -> None:
    policy = load_layer_policy()

    assert dependency_allowed("110-examples", "070-facade", policy)
    assert dependency_allowed("120-tests", "070-facade", policy)
    assert dependency_allowed("120-tests", "110-examples", policy)
    assert not dependency_allowed("070-facade", "110-examples", policy)
    assert not dependency_allowed("070-facade", "120-tests", policy)
    assert not dependency_allowed("110-examples", "120-tests", policy)



def test_dependency_rules_cover_every_layer_and_reject_upward_edges() -> None:
    policy = load_layer_policy()

    assert all(isinstance(rule, DependencyRule) for rule in policy.dependency_rules)
    assert set(policy.rules_by_consumer) == set(EXPECTED_LAYER_ORDER)
    assert dependency_allowed("050-protocols", "040-capabilities", policy)
    assert dependency_allowed("010-concrete", "003-codecs", policy)
    assert dependency_allowed("020-providers", "003-codecs", policy)
    assert dependency_allowed("030-storage-runtime", "003-codecs", policy)
    assert dependency_allowed("120-tests", "003-codecs", policy)
    assert not dependency_allowed("003-codecs", "020-providers", policy)
    assert not dependency_allowed("020-providers", "040-capabilities", policy)
    assert not dependency_allowed("060-runtime", "080-routers", policy)
    assert dependency_allowed("090-backend-apps", "080-routers", policy)


def test_package_exceptions_are_eliminated_and_path_classification_is_authoritative() -> None:
    policy = load_layer_policy()

    assert classify_layer(ROOT / "pkgs" / "080-routers" / "example", policy) == "080-routers"
    assert not package_dependency_allowed(
        "tba-runtime-identity",
        "060-runtime",
        "tba-router-webauthn",
        "080-routers",
        policy,
    )
    assert not package_dependency_allowed(
        "tba-server-identity",
        "060-runtime",
        "tba-router-session-login",
        "080-routers",
        policy,
    )
    assert package_dependency_allowed(
        "tba-app-backend-core",
        "090-backend-apps",
        "tba-router-session-login",
        "080-routers",
        policy,
    )
    assert policy.dependency_exceptions == ()
    assert not package_dependency_allowed(
        "new-runtime", "060-runtime", "new-router", "080-routers", policy
    )

def test_duplicate_layer_ids_are_rejected(tmp_path: Path) -> None:
    policy_path = tmp_path / "layers.toml"
    policy_path.write_text(
        """schema_version = 1
[[layers]]
id = \"010-concrete\"
order = 10
category = \"production\"
[[layers]]
id = \"010-concrete\"
order = 20
category = \"production\"
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="ids must be unique"):
        load_layer_policy(policy_path)
