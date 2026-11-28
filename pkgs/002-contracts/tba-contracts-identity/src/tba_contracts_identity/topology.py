"""Identity topology scenario contracts.

These scenarios describe deployment data shape. They are intentionally separate
from runtime certification profiles such as baseline, production, and hardening.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

AxisCardinality = Literal["single", "multi"]


@dataclass(frozen=True, slots=True)
class IdentityTopologyScenario:
    id: int
    realm: AxisCardinality
    tenant: AxisCardinality
    identities: AxisCardinality

    def as_tuple(self) -> tuple[AxisCardinality, AxisCardinality, AxisCardinality]:
        return (self.realm, self.tenant, self.identities)


IDENTITY_TOPOLOGY_SCENARIOS: tuple[IdentityTopologyScenario, ...] = (
    IdentityTopologyScenario(1, "single", "single", "single"),
    IdentityTopologyScenario(2, "single", "single", "multi"),
    IdentityTopologyScenario(3, "single", "multi", "single"),
    IdentityTopologyScenario(4, "single", "multi", "multi"),
    IdentityTopologyScenario(5, "multi", "single", "single"),
    IdentityTopologyScenario(6, "multi", "single", "multi"),
    IdentityTopologyScenario(7, "multi", "multi", "single"),
    IdentityTopologyScenario(8, "multi", "multi", "multi"),
)

IDENTITY_TOPOLOGY_BY_ID: dict[int, IdentityTopologyScenario] = {
    scenario.id: scenario for scenario in IDENTITY_TOPOLOGY_SCENARIOS
}


def identity_topology_scenario(scenario_id: int) -> IdentityTopologyScenario:
    try:
        return IDENTITY_TOPOLOGY_BY_ID[int(scenario_id)]
    except KeyError as exc:
        raise ValueError(f"unknown identity topology scenario id: {scenario_id}") from exc


def cardinality_for_count(count: int) -> AxisCardinality | None:
    if count == 1:
        return "single"
    if count > 1:
        return "multi"
    return None


__all__ = [
    "AxisCardinality",
    "IDENTITY_TOPOLOGY_BY_ID",
    "IDENTITY_TOPOLOGY_SCENARIOS",
    "IdentityTopologyScenario",
    "cardinality_for_count",
    "identity_topology_scenario",
]
