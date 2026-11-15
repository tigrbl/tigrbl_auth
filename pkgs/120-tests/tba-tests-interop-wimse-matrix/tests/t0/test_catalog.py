import pytest

from tba_test_interop_wimse.__main__ import accepts, load_catalog, references
from tba_test_interop_wimse.catalog import read_catalog, validate_catalog
from tba_test_interop_wimse.matrix import validate_events

FACTORS, RULES = load_catalog()
DOMAINS = {key: factor["levels"] for key, factor in FACTORS.items()}


@pytest.mark.parametrize("key,level", [(key, value) for key, levels in DOMAINS.items()
                                      for value in levels])
def test_factor_levels(key, level):
    assert isinstance(level, str) and level.strip() == level and level
    assert DOMAINS[key].count(level) == 1


@pytest.mark.parametrize("rule", RULES, ids=lambda rule: rule["id"])
def test_rule_has_allowed_and_excluded_assignments(rule):
    from itertools import product

    keys = sorted(references(rule["when"], DOMAINS)
                  | references(rule.get("requires", rule.get("excludes")), DOMAINS))
    outcomes = {accepts(rule, dict(zip(keys, values)))
                for values in product(*(DOMAINS[key] for key in keys))}
    assert outcomes == {True, False}


def test_catalog_and_event_contract():
    scenarios = read_catalog("scenarios.toml")
    validate_catalog(read_catalog("factors.toml"), scenarios, read_catalog("exclusions.toml"))
    for family in scenarios["scenarios"]:
        for variant in family["variants"]:
            validate_events(family["id"], variant)
    with pytest.raises(ValueError, match="event ordering"):
        validate_events("12", {"id": "revocation-before-effect",
                               "events": ["revocation-observed", "initial-allow", "commit-refused"]})
