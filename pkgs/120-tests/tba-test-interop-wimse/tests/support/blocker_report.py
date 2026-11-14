"""Summarize remaining candidate blockers for a pinned lab snapshot."""

import argparse
from collections import Counter
import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory

from tba_test_interop_wimse.evidence import audit_pytest_report
from tba_test_interop_wimse.matrix import generate_matrix

from support.wimsey_endpoint import WimseyWicAdapter


def blocker_report(matrix, adapter, results):
    scenarios = {case["id"]: case for case in matrix["scenarios"]}
    overlaps, baselines, sole_baselines, support, families = (Counter() for _ in range(5))
    for execution in matrix["executions"]:
        if results[execution["id"]]["status"] == "passed":
            continue
        case = scenarios[execution["scenario_id"]]
        categories = []
        if not (adapter.supports(case) and adapter.supports_execution(case, execution)):
            categories.append("adapter")
        if execution["missing_baselines"]:
            categories.append("baseline")
        if execution["pending_roles"]:
            categories.append("issuer/support")
        overlaps[" + ".join(categories) or "runtime outcome"] += 1
        families[case["scenario_id"]] += 1
        support.update(set(execution["pending_roles"]))
        missing = set()
        for hop in execution["missing_baselines"]:
            caller, receiver = (execution["pairs"][hop][role] for role in ("caller", "receiver"))
            missing.add(f"{caller['implementation']} → {receiver['implementation']} "
                        f"({caller['profile']}, {caller['identifier_scheme']})")
        baselines.update(missing)
        if len(missing) == 1:
            sole_baselines.update(missing)
    return {
        "overlap": dict(overlaps),
        "by_category": {
            name: sum(count for overlap, count in overlaps.items() if name in overlap.split(" + "))
            for name in ("adapter", "baseline", "issuer/support")
        },
        "by_missing_baseline": dict(baselines.most_common()),
        "by_sole_missing_baseline": dict(sole_baselines.most_common()),
        "by_missing_issuer_or_support_role": dict(support.most_common()),
        "by_family": dict(families.most_common()),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("snapshot", type=Path)
    parser.add_argument("junit", type=Path)
    args = parser.parse_args()
    snapshot = json.loads(args.snapshot.read_text(encoding="utf-8"))
    matrix = generate_matrix(peers=snapshot["peers"])
    audited = audit_pytest_report(matrix["executions"], args.junit)
    with TemporaryDirectory(dir=args.snapshot.resolve().parent) as directory:
        adapter = WimseyWicAdapter(directory, os.environ["TBA_WIMSEY_CHECKOUT"])
        if adapter.binary_sha256 != snapshot["wimsey_binary_sha256"]:
            raise ValueError("wimsey binary differs from the qualified snapshot")
        report = blocker_report(matrix, adapter, audited["results"])
    print(json.dumps({"required": audited["required"], "outcomes": audited["counts"],
                      **report}, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
