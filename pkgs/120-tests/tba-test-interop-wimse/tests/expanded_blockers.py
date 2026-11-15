"""Export per-ID blockers and runtime history for an expanded WIMSE manifest."""

import argparse
import csv
import gzip
import json
from collections import Counter
from pathlib import Path

from tba_test_interop_wimse.evidence import audit_pytest_report
from tba_test_interop_wimse.native_expansion import (
    COMBINED_RECORD, COMBINED_SCOPE, NATIVE_ISSUERS, expanded_plan, matches_native_issuer_scope,
)
from tba_test_interop_wimse.qualification import pair_has_baseline
from external_workload_selection import spiffe_support_rows
from typed_service_selection import (
    native_acquisition_rows, native_baseline_policy_rows, native_svid_policy_rows, typed_service_rows,
)


def rows(plan):
    return plan["workload_executions"] + plan["planned_executions"]


def case_key(row):
    def pin(values):
        if values[0] in {"go-spiffe", "defakto"}:
            return [values[0], None, None]
        return [values[0], None if values[0] == "tba" else values[1], values[2]]

    if "pairs" in row:
        bindings = [
            pin([endpoint[key] if key in endpoint else None for key in ("implementation", "version", "configuration")])
            for pair in row["pairs"].values() for endpoint in (pair["caller"], pair["receiver"])
        ]
        return json.dumps([row["scenario_id"], bindings])
    hops = [
        {key: pin(value) if key.endswith("_pin") else value for key, value in hop.items()}
        for hop in row["hops"]
    ]
    return json.dumps([row["outcome_id"], hops], sort_keys=True)


def pending_typed_bindings(row, peers, by_capability, *, service_qualified=False):
    endpoints, baselines, issuers, support = set(), set(), set(), set()
    local_operations = {("check",), ("delegate",)}
    path = tuple(hop["operation"] for hop in row["hops"])
    native_control = path == ("call",) * 3 and row.get("native_stage") == "baseline-issuer"
    if path == ("call",) * 3 and row.get("native_stage") == "native-svid":
        qualified = set()
        for issuer, (field, key) in NATIVE_ISSUERS.items():
            record = peers.get(key, {})
            profiles = {tuple(profile) for profile in record.get("profiles", ())}
            if record.get("evidence") and all(
                (hop["profile"], hop["identifier_scheme"]) in profiles
                and all(hop[f"{role}_pin"][1] == record["version"] for role in ("caller", "receiver"))
                for hop in row["hops"] if hop[field] == issuer
            ):
                qualified.add(issuer)
        native_control = any(matches_native_issuer_scope(row["hops"], issuer) for issuer in qualified)
        combined = peers.get(COMBINED_RECORD, {})
        if NATIVE_ISSUERS.keys() <= qualified and combined.get("evidence"):
            profiles = {tuple(profile) for profile in combined.get("profiles", ())}
            native_control |= matches_native_issuer_scope(row["hops"], COMBINED_SCOPE) and all(
                (hop["profile"], hop["identifier_scheme"]) in profiles
                and all(hop[f"{role}_pin"][1] == combined["version"] for role in ("caller", "receiver"))
                for hop in row["hops"] if matches_native_issuer_scope([hop], COMBINED_SCOPE)
            )
    for index, hop in enumerate(row["hops"], 1):
        pair = {}
        if "profile" in hop:
            for role in ("caller", "receiver"):
                pin = tuple(hop[f"{role}_pin"])
                cap = by_capability.get((*pin, role, hop["profile"], hop["identifier_scheme"]))
                if cap and cap["status"] == "qualified":
                    pair[role] = cap
                else:
                    endpoints.add(f"{index}:{role}:{pin[0]}")
            # Native baseline-issuer three-call cases exercise the actual
            # native endpoints as controls and have their own observed evidence.
            if not native_control and (len(pair) < 2 or not pair_has_baseline(peers, pair)):
                baselines.add(str(index))
            for kind in ("wic_issuer", "wit_issuer"):
                issuer = hop[kind]
                if issuer == "none" or native_control:
                    continue
                qualified = peers.get("qualified_support", {}).get(f"enforcing:{kind}:{issuer}", {})
                if not any(b.get("profile") == hop["profile"]
                           and hop["identifier_scheme"] in b.get("identifier_schemes", ())
                           and all(endpoint["configuration"] == b.get("endpoint_configuration", b.get("configuration"))
                                   for endpoint in pair.values())
                           for b in qualified.get("bindings", [qualified])):
                    issuers.add(f"{index}:{kind}:{issuer}")
        elif "support" in hop and path not in local_operations:
            support.add(f"{index}:{hop['support']}")
    registered = path in local_operations or native_control or (
        path == ("call",) * 3 and not row.get("native_stage")
    )
    if service_qualified:
        registered = True
        support.clear()
        if row.get("native_stage"):
            baselines.clear()
            issuers.clear()
    if path == ("check",) and row["outcome_id"] not in {
        "success", "1:revoked-status-refused", "1:stale-status-refused", "1:unavailable-status-refused",
    }:
        registered = False
    return endpoints, baselines, issuers, support, "" if registered else " > ".join(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--snapshot", type=Path, required=True)
    parser.add_argument("--history", nargs=2, action="append", default=[], metavar=("SNAPSHOT", "JUNIT"))
    parser.add_argument("--live-attempts", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    with gzip.open(args.manifest, "rt", encoding="utf-8") as source:
        published = rows(json.load(source))
    expected = {case_key(row): row["id"] for row in published}
    if len(expected) != len(published):
        raise ValueError("Published manifest has duplicate logical cases")
    snapshot = json.loads(args.snapshot.read_text(encoding="utf-8"))
    peers = snapshot["peers"]
    plan = expanded_plan(peers, include_candidates=True, include_native=True, include_executions=True)
    current = rows(plan)
    qualified_services = ({row["id"] for row in typed_service_rows(plan)}
                          if snapshot.get("typed_service_qualification") else set())
    if snapshot.get("native_acquisition_qualification"):
        qualified_services.update(row["id"] for row in native_acquisition_rows(plan))
    if snapshot.get("native_specialized_acquisition_qualification"):
        qualified_services.update(row["id"] for row in native_acquisition_rows(plan, specialized=True))
    if snapshot.get("native_baseline_policy", {}).get("evidence"):
        qualified_services.update(row["id"] for row in native_baseline_policy_rows(plan))
    if snapshot.get("native_svid_policy", {}).get("evidence"):
        qualified_services.update(row["id"] for row in native_svid_policy_rows(plan))
    for name, support in (("emilia", "emilia"), ("mintid", "mintid"), ("teleport", "teleport-tbot")):
        if snapshot.get(f"{name}_qualification"):
            qualified_services.update(row["id"] for row in spiffe_support_rows(plan, support))
    by_id = {row["id"]: row for row in current}
    published_ids = {row["id"]: expected[case_key(row)] for row in current}
    if len(by_id) != len(expected) or len(set(published_ids.values())) != len(expected):
        raise ValueError("Runtime snapshot must match the published logical inventory")
    evidence = {}
    for snapshot, junit in args.history:
        history_peers = json.loads(Path(snapshot).read_text(encoding="utf-8"))["peers"]
        history = rows(expanded_plan(history_peers, include_candidates=True, include_native=True, include_executions=True))
        by_history_id = {row["id"]: row for row in history}
        audit = audit_pytest_report(history, junit)
        for identifier, record in audit["results"].items():
            if not record["attempts"]:
                continue
            published_id = expected[case_key(by_history_id[identifier])]
            status = record["status"]
            if status == "passed" or evidence.get(published_id, {}).get("status") != "passed":
                evidence[published_id] = dict(record["attempts"][-1], report=junit)
    latest = {}
    if args.live_attempts:
        with args.live_attempts.open(encoding="utf-8") as source:
            for line in source:
                if not line.endswith("\n"):
                    break  # Ignore a record still being appended by the live runner.
                attempt = json.loads(line)
                latest[attempt["execution_id"]] = attempt
        if latest.keys() - by_id.keys():
            raise ValueError("Live attempts contain IDs outside the runtime snapshot")

    caps = {tuple(row.get(key) for key in ("implementation", "version", "configuration", "role",
                                          "profile", "identifier_scheme")): row for row in peers["capabilities"]}
    fields = ("execution_id", "runtime_id", "scope", "hop_sequence_id", "operation_path", "status",
              "historical_status", "historical_runtime_id", "historical_report", "endpoint_gaps",
              "directional_baseline_gaps", "issuer_gaps", "support_role_gaps", "missing_adapter", "reason")
    counts = Counter()
    with gzip.open(args.output, "wt", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        for row in current:
            runtime_id = row["id"]
            identifier = published_ids[runtime_id]
            history = evidence.get(identifier, {})
            attempt = latest.get(runtime_id, history if history.get("execution_id") == runtime_id else {})
            if "pairs" in row:
                path = ["call"] * row["hop_count"]
                endpoints, baselines = row["pending_endpoints"], row["missing_baselines"]
                issuers = [role for role in row["pending_roles"] if "_issuer:" in role]
                support = [role for role in row["pending_roles"] if "_issuer:" not in role]
                missing = "native scenario adapter" if row.get("native_stage") and row["status"] != "qualified" else ""
            else:
                path = [hop["operation"] for hop in row["hops"]]
                endpoints, baselines, issuers, support, missing = pending_typed_bindings(
                    row, peers, caps, service_qualified=runtime_id in qualified_services,
                )
            inferred = "blocked" if any((endpoints, baselines, issuers, support, missing)) else "runnable"
            status = attempt.get("status", inferred)
            counts[status] += 1
            writer.writerow({
                "execution_id": identifier, "runtime_id": runtime_id,
                "scope": row.get("native_stage", "external"), "hop_sequence_id": row["hop_sequence_id"],
                "operation_path": " > ".join(path), "status": status,
                "historical_status": history.get("status", ""), "historical_runtime_id": history.get("execution_id", ""),
                "historical_report": history.get("report", ""), "endpoint_gaps": " | ".join(sorted(endpoints)),
                "directional_baseline_gaps": " | ".join(sorted(baselines)), "issuer_gaps": " | ".join(sorted(issuers)),
                "support_role_gaps": " | ".join(sorted(support)), "missing_adapter": missing,
                "reason": attempt.get("reason", ""),
            })
    print(json.dumps({"rows": sum(counts.values()), "statuses": counts,
                      "historical_passes": sum(r["status"] == "passed" for r in evidence.values()),
                      "live_attempts": len(latest)}, sort_keys=True))


if __name__ == "__main__":
    main()
