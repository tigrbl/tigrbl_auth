from __future__ import annotations

import pytest

from tigrbl_identity_contracts.topology import (
    IDENTITY_TOPOLOGY_BY_ID,
    IDENTITY_TOPOLOGY_SCENARIOS,
    cardinality_for_count,
    identity_topology_scenario,
)


def test_identity_topology_matrix_matches_supported_realm_tenant_identity_scenarios() -> None:
    assert [scenario.id for scenario in IDENTITY_TOPOLOGY_SCENARIOS] == list(range(1, 9))
    assert [scenario.as_tuple() for scenario in IDENTITY_TOPOLOGY_SCENARIOS] == [
        ("single", "single", "single"),
        ("single", "single", "multi"),
        ("single", "multi", "single"),
        ("single", "multi", "multi"),
        ("multi", "single", "single"),
        ("multi", "single", "multi"),
        ("multi", "multi", "single"),
        ("multi", "multi", "multi"),
    ]
    assert set(IDENTITY_TOPOLOGY_BY_ID) == set(range(1, 9))


def test_identity_topology_lookup_rejects_unknown_scenario_ids() -> None:
    assert identity_topology_scenario(8).realm == "multi"

    with pytest.raises(ValueError, match="unknown identity topology scenario id"):
        identity_topology_scenario(9)


def test_cardinality_for_count_keeps_zero_outside_supported_matrix() -> None:
    assert cardinality_for_count(0) is None
    assert cardinality_for_count(1) == "single"
    assert cardinality_for_count(2) == "multi"
