"""Identify catalog rows without executable coverage."""
def coverage_report(matrix, adapters):
    assigned = {row["scenario_id"] for row in matrix["executions"]}
    cases = matrix["scenarios"]
    return {
        "no_candidate": [case["id"] for case in cases if case["id"] not in assigned],
        "no_adapter": [
            case["id"] for case in cases
            if case["scenario_id"] not in adapters or not adapters[case["scenario_id"]].supports(case)
        ],
        "unqualified": [row["id"] for row in matrix["executions"] if row["status"] != "qualified"],
    }
