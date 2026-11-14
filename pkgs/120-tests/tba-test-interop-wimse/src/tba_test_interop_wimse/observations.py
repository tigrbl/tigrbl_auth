"""Evaluate scenario outcomes against observed state."""
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Observation:
    decision: str
    hop: str
    events: tuple[str, ...] = ()
    effects: int = 0
    releases: int = 0
    additional_effects: int = 0
    budget_limit: int | None = None
    reason: str = ""
    measurements: dict[str, int] = field(default_factory=dict)


def mismatches(case, observed):
    errors = []
    events = tuple(case["events"])
    if observed.hop != case["target_hop"]:
        errors.append("wrong enforcing hop")
    if observed.decision != case["decision"]:
        errors.append("wrong decision")
    if events and observed.events != events:
        errors.append("wrong event sequence")
    if "bearer-released" in events and observed.releases != 1:
        errors.append("expected one bearer release")
    if case["scenario_id"] == "18" and case["decision"] == "deny" and observed.releases:
        errors.append("unexpected bearer release")
    effect = case["effect"]
    if effect == "zero-effects" and observed.effects != 0:
        errors.append("unexpected effect")
    if effect == "one-intended-effect" and observed.effects != 1:
        errors.append("expected one effect")
    if effect == "zero-additional-effects" and observed.additional_effects != 0:
        errors.append("unexpected additional effect")
    if effect == "committed-effects-at-or-below-limit" and (
        observed.budget_limit is None or observed.effects > observed.budget_limit
    ):
        errors.append("shared limit exceeded or missing")
    if effect == "shared-limit-may-be-exceeded" and (
        observed.budget_limit is None or observed.effects <= observed.budget_limit
    ):
        errors.append("fixture did not exercise excess effects")
    return errors
