"""Count WIMSE matrix tuples without materializing the Cartesian product."""

import argparse
import json
from importlib.resources import files
from itertools import product

try:
    import tomllib
except ModuleNotFoundError:  # Python 3.10
    import tomli as tomllib

from .matrix import generate_matrix
from .coverage import inventory_report
from .evidence import audit_pytest_report
from pathlib import Path


def matches(expression, assignment):
    if "factor" in expression:
        return assignment[expression["factor"]] in expression["in"]
    if "not" in expression:
        return not matches(expression["not"], assignment)
    if "all" in expression:
        return all(matches(child, assignment) for child in expression["all"])
    return any(matches(child, assignment) for child in expression["any"])


def references(expression, domains):
    if "factor" in expression:
        factor = expression["factor"]
        if not set(expression["in"]) <= set(domains[factor]):
            raise ValueError(f"Unknown level for {factor}: {expression['in']}")
        return {factor}
    if "not" in expression:
        return references(expression["not"], domains)
    children = expression["all"] if "all" in expression else expression["any"]
    return set.union(*(references(child, domains) for child in children))


def accepts(rule, assignment):
    if not matches(rule["when"], assignment):
        return True
    if "requires" in rule:
        return matches(rule["requires"], assignment)
    return not matches(rule["excludes"], assignment)


def count_combinations(domains, rules):
    """Sum over one factor at a time, keeping counts for its remaining neighbors."""
    scopes = [
        tuple(sorted(references(rule["when"], domains) |
                     references(rule.get("requires", rule.get("excludes")), domains)))
        for rule in rules
    ]
    tables = []
    for scope, rule in zip(scopes, rules):
        allowed = {}
        for values in product(*(domains[key] for key in scope)):
            if accepts(rule, dict(zip(scope, values))):
                allowed[values] = 1
        tables.append((scope, allowed))

    remaining = set(domains)
    total = 1
    while remaining:
        def neighbors(key):
            return set().union(*(scope for scope, _ in tables if key in scope)) - {key}

        key = min(remaining, key=lambda name: (
            product_size(domains, neighbors(name) | {name}), name
        ))
        neighbor_scope = tuple(sorted(neighbors(key)))
        affected = [(scope, table) for scope, table in tables if key in scope]
        tables = [(scope, table) for scope, table in tables if key not in scope]
        scope = (*neighbor_scope, key)
        positions = {name: index for index, name in enumerate(scope)}
        lookups = [(tuple(positions[name] for name in names), table)
                   for names, table in affected]
        counts = {}
        for neighbors_values in product(*(domains[name] for name in neighbor_scope)):
            subtotal = 0
            for level in domains[key]:
                values = (*neighbors_values, level)
                subtotal += multiply(table.get(tuple(values[i] for i in indices), 0)
                                     for indices, table in lookups)
            if subtotal:
                counts[neighbors_values] = subtotal
        if neighbor_scope:
            tables.append((neighbor_scope, counts))
        else:
            total *= counts.get((), 0)
        remaining.remove(key)
    return total


def multiply(values):
    result = 1
    for value in values:
        result *= value
        if not result:
            break
    return result


def product_size(domains, keys):
    return multiply(len(domains[key]) for key in keys)


def load_catalog():
    """Load the versioned factor catalog and its companion exclusions."""
    resources = files("tba_test_interop_wimse")
    with resources.joinpath("factors.toml").open("rb") as catalog:
        model = tomllib.load(catalog)
    with resources.joinpath(model["exclusions_file"]).open("rb") as exclusion_file:
        exclusions = tomllib.load(exclusion_file)
    if model["schema_version"] != 1 or exclusions["schema_version"] != 1:
        raise ValueError("Unsupported WIMSE interop catalog schema version")
    if any("requires" not in rule or "excludes" in rule for rule in model["rules"]):
        raise ValueError("Factor rules must contain requires")
    if any("excludes" not in rule or "requires" in rule for rule in exclusions["rules"]):
        raise ValueError("Exclusion rules must contain excludes")
    return model["factors"], [*model["rules"], *exclusions["rules"]]


def main():
    parser = argparse.ArgumentParser(description="Generate WIMSE interop coverage")
    parser.add_argument("--json", action="store_true", help="export scenario and execution rows")
    parser.add_argument("--legacy-count", action="store_true", help="count the flat factor model")
    parser.add_argument("--coverage", action="store_true", help="export coverage and attempt status by ID")
    parser.add_argument("--attempts", type=Path, help="JSON array of peer execution attempts")
    parser.add_argument("--audit-peer-junit", type=Path,
                        help="audit per-execution results and require every candidate to pass")
    parser.add_argument("--peer-snapshot", type=Path, help="audit against an explicit lab qualification snapshot")
    options = parser.parse_args()
    if options.attempts and not options.coverage:
        parser.error("--attempts requires --coverage")
    if options.audit_peer_junit:
        try:
            peers = (json.loads(options.peer_snapshot.read_text(encoding="utf-8"))["peers"]
                     if options.peer_snapshot else None)
            report = audit_pytest_report(generate_matrix(peers=peers)["executions"], options.audit_peer_junit)
        except (ValueError, KeyError, OSError) as error:
            parser.error(str(error))
        if not options.json:
            report.pop("results")
        print(json.dumps(report, ensure_ascii=True))
        if not report["complete"]:
            raise SystemExit(1)
        return
    if options.coverage:
        attempts = json.loads(options.attempts.read_text(encoding="utf-8")) if options.attempts else []
        print(json.dumps(inventory_report(generate_matrix(), attempts), ensure_ascii=True))
        return
    if not options.legacy_count:
        matrix = generate_matrix()
        if options.json:
            print(json.dumps(matrix, ensure_ascii=True))
        else:
            for label, count in matrix["counts"].items():
                print(f"{label.replace('_', ' ').capitalize()}: {count:,}")
        return
    factors, rules = load_catalog()
    domains = {key: factor["levels"] for key, factor in factors.items()}
    for key, levels in domains.items():
        if not levels or len(levels) != len(set(levels)):
            raise ValueError(f"Empty or duplicate levels for {key}")
    if len({rule["id"] for rule in rules}) != len(rules):
        raise ValueError("Duplicate rule IDs")
    raw = product_size(domains, domains)
    allowed = count_combinations(domains, rules)
    print(f"Raw combinations: {raw:,}")
    print(f"Allowed by stored rules: {allowed:,}")
    print(f"Excluded by stored rules: {raw - allowed:,}")


if __name__ == "__main__":
    main()
