"""Enumerate hop type sequences and join them to structural scenarios."""

from collections import Counter, defaultdict
from itertools import product

from .catalog import read_catalog


def sequence_id(types):
    return "+".join(types)


def generate_hop_matrix(matrix):
    catalog = read_catalog("hops.toml")
    types = catalog["types"]
    candidates = {
        sequence_id(sequence): sequence
        for length in range(1, catalog["max_hops"] + 1)
        for sequence in product(types, repeat=length)
    }
    examples = {}
    for shape in catalog["shapes"]:
        key = sequence_id(shape["sequence"])
        if key not in candidates or key in examples:
            raise ValueError(f"Unknown or duplicate hop sequence: {key}")
        examples[key] = shape["example"]

    scenarios_by_sequence = defaultdict(list)
    for case in matrix["scenarios"]:
        key = case["hop_sequence_id"]
        if key not in candidates:
            raise ValueError(f"Unrecognized scenario hop sequence: {key}")
        scenarios_by_sequence[key].append(case)
    run_counts = Counter(row["hop_sequence_id"] for row in matrix["executions"])
    qualified_counts = Counter(
        row["hop_sequence_id"] for row in matrix["executions"] if row["status"] == "qualified"
    )

    rows = []
    for key, sequence in candidates.items():
        scenarios = scenarios_by_sequence[key]
        status = "mapped" if scenarios else "proposed" if key in examples else "unreviewed"
        rows.append({
            "hop_sequence_id": key,
            "hop_count": len(sequence),
            "hop_types": sequence,
            "status": status,
            "scenario_family_ids": sorted({case["scenario_id"] for case in scenarios}),
            "structural_scenarios": len(scenarios),
            "candidate_runs": run_counts[key],
            "qualified_runs": qualified_counts[key],
            "binding_gaps": [] if scenarios else [
                types[kind]["binding_gap"] for kind in dict.fromkeys(sequence)
            ],
            "example": examples.get(key, ""),
        })
    return {"types": types, "composition": catalog["composition"], "sequences": rows}
