"""Identify catalog rows without executable coverage."""
from .catalog import read_catalog, validate_fixture_manifest
from .evidence import reconcile


def inventory_report(matrix, attempts=()):
    manifest = read_catalog("fixtures.toml")
    cases = {case["id"]: case for case in matrix["scenarios"]}
    profiles = read_catalog("factors.toml")["hop_profiles"]
    validate_fixture_manifest(manifest, {case["scenario_id"] for case in cases.values()}, profiles)
    executions = matrix["executions"]
    history = reconcile([row["id"] for row in executions], attempts)

    def bindings(case, section, direction=None):
        if len(case["hops"]) != 1:
            return []
        hop = case["hops"][case["target_hop"]]
        return [
            name for name, item in manifest[section].items()
            if case["scenario_id"] in item["families"]
            and (item["profile"], item["identifier_scheme"]) == (hop["profile"], hop["identifier_scheme"])
            and item.get("direction", direction) == direction
            and item["issuer"] in (hop["wic_issuer"], hop["wit_issuer"])
            and ("variants" not in item or case["variant"] in item["variants"])
            and (not item.get("require_baseline_issuers") or all(
                hop[key] in {"baseline", "none"} for key in ("wic_issuer", "wit_issuer")
            ))
        ]

    return {
        "scenarios": [
            {"id": case["id"], "local_fixtures": bindings(case, "local")}
            for case in cases.values()
        ],
        "executions": [
            {
                "id": row["id"],
                "qualification": row["status"],
                "pending_roles": row["pending_roles"],
                "component_fixtures": bindings(cases[row["scenario_id"]], "peer", row["direction"]),
                **history[row["id"]],
            }
            for row in executions
        ],
    }


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
