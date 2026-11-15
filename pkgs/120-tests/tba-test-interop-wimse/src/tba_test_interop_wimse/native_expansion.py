"""Join the external peer matrix and its planned all-TbA counterpart."""

from collections import Counter

from .catalog import read_catalog
from .hop_expansion import hop_execution_id, include_candidate_endpoints, plan_hop_expansion
from .matrix import generate_matrix


NATIVE_ISSUERS = {
    "tba-wit-svid": ("wit_issuer", "native_wit_svid"),
    "tba-x509-svid": ("wic_issuer", "native_x509_svid"),
}
COMBINED_SCOPE = "combined"
COMBINED_RECORD = "native_combined_svid"
BASELINE_WORKLOAD_RECORD = "native_baseline_workload"


def native_baseline_workload_rows(plan):
    return [row for row in plan["workload_executions"] if row.get("native_stage") == "baseline-issuer"]


def matches_native_issuer_scope(hops, issuer):
    present = {
        hop[field] for hop in hops for field, _ in NATIVE_ISSUERS.values()
        if hop[field] in NATIVE_ISSUERS
    }
    required = NATIVE_ISSUERS.keys() if issuer == COMBINED_SCOPE else {issuer}
    return present == required


def native_issuer_rows(plan, issuer):
    scenarios = {row["id"]: row for row in plan["scenario_definitions"]}
    workloads = [
        row for row in plan["workload_executions"]
        if row.get("native_stage") == "native-svid"
        and matches_native_issuer_scope(scenarios[row["scenario_id"]]["hops"].values(), issuer)
    ]
    typed = [
        row for row in plan["planned_executions"]
        if row.get("native_stage") == "native-svid"
        and tuple(hop["operation"] for hop in row["hops"]) == ("call",) * 3
        and matches_native_issuer_scope(row["hops"], issuer)
    ]
    return workloads, typed


def native_operation_catalog():
    catalog = read_catalog("hops.toml")
    operations = catalog["operations"]
    native = catalog["native"]
    equivalents = native["equivalent_operations"]
    for name, changes in native["overrides"].items():
        operations[name].update(changes)
    for name, replacement in equivalents.items():
        operation = dict(operations[name])
        del operation["candidate"]
        del operation["candidate_role"]
        operations[replacement["operation"]] = {
            **operation, **{key: value for key, value in replacement.items() if key != "operation"},
        }
    for operation in operations.values():
        following = operation["next"]
        operation["next"] = following + [equivalents[name]["operation"] for name in following if name in equivalents]
    return catalog


def expanded_plan(peers, *, include_candidates=False, include_native=False, include_executions=False):
    peers = include_candidate_endpoints(peers) if include_candidates else peers
    matrix = generate_matrix(peers=peers)
    report = plan_hop_expansion(
        matrix, peers, include_candidates=include_candidates,
        include_executions=include_executions or include_native,
    )
    if include_native:
        add_native_runs(report, matrix["scenarios"], peers)
    if include_executions:
        report.setdefault("scenario_definitions", matrix["scenarios"])
    else:
        report.pop("workload_executions", None)
        report.pop("planned_executions", None)
        report.pop("scenario_definitions", None)
    return report


def add_native_runs(report, external_scenarios, peers):
    catalog = native_operation_catalog()
    issuers = catalog["native"]["issuers"]
    equivalent_paths = {row["operation"] for row in catalog["native"]["equivalent_operations"].values()}
    native_matrix = generate_matrix(peers=peers, native_only=True)
    native_report = plan_hop_expansion(
        native_matrix, peers, catalog=catalog, native_only=True, include_executions=True,
    )
    seen = {row["id"] for key in ("workload_executions", "planned_executions") for row in report[key]}
    native_counts = Counter()
    stages = Counter()
    shared = 0

    def project_key(identifier):
        for previous, native_issuer in issuers.items():
            identifier = identifier.replace(previous, native_issuer)
        return identifier

    def project_issuers(hop):
        return {key: issuers.get(value, value) if key in ("wic_issuer", "wit_issuer") else value
                for key, value in hop.items()}

    scenarios = {row["id"]: row for row in external_scenarios}
    for row in native_matrix["scenarios"]:
        identifier = project_key(row["id"])
        scenarios.setdefault(identifier, {
            **row, "id": identifier,
            "hops": {name: project_issuers(hop) for name, hop in row["hops"].items()},
        })
    controls = {}
    for issuer, (field, key) in NATIVE_ISSUERS.items():
        record = peers.get(key, {})
        if record.get("evidence"):
            controls[issuer] = (field, record["version"], {tuple(profile) for profile in record["profiles"]})
    combined = peers.get(COMBINED_RECORD, {})
    scopes = {issuer: (version, {issuer}) for issuer, (_, version, _) in controls.items()}
    if combined.get("evidence") and all(
        issuer in controls and controls[issuer][1] == combined["version"] for issuer in NATIVE_ISSUERS
    ):
        scopes[COMBINED_SCOPE] = (combined["version"], NATIVE_ISSUERS.keys())

    def profile_qualified(hop, required):
        profile = hop["profile"], hop["identifier_scheme"]
        if (required == NATIVE_ISSUERS.keys() and hop["wic_issuer"] == "tba-x509-svid"
                and hop["wit_issuer"] == "tba-wit-svid"
                and profile not in combined_profiles):
            return False
        return all(hop[field] != issuer or profile in profiles
                   for issuer, (field, _, profiles) in controls.items() if issuer in required)

    combined_profiles = {tuple(profile) for profile in combined.get("profiles", ())}
    baseline = peers.get(BASELINE_WORKLOAD_RECORD, {})
    baseline_profiles = {tuple(profile) for profile in baseline.get("profiles", ())}
    for row in native_report["workload_executions"]:
        identifier = project_key(row["id"])
        stage = "native-svid" if identifier != row["id"] else "baseline-issuer"
        if identifier in seen:
            raise ValueError(f"Duplicate all-TbA workload execution: {identifier}")
        seen.add(identifier)
        scenario_id = project_key(row["scenario_id"])
        hops = scenarios[scenario_id]["hops"].values()
        pending = [project_key(role) for role in row["pending_roles"]]
        qualified = any(
            matches_native_issuer_scope(hops, scope)
            and all(profile_qualified(hop, required) for hop in hops)
            and all(endpoint["status"] == "qualified" and endpoint.get("version") == version
                    for pair in row["pairs"].values() for endpoint in pair.values())
            and all(role.rpartition(":")[2] in required for role in pending)
            for scope, (version, required) in scopes.items()
        )
        if stage == "baseline-issuer" and baseline.get("evidence"):
            qualified = not pending and all(
                endpoint["status"] == "qualified" and endpoint["implementation"] == "tba"
                and endpoint.get("version") == baseline["version"]
                and (endpoint["profile"], endpoint["identifier_scheme"], endpoint["configuration"])
                in baseline_profiles
                for pair in row["pairs"].values() for endpoint in pair.values()
            )
        report["workload_executions"].append({
            **row, "id": identifier, "scenario_id": scenario_id,
            "native_stage": stage, "status": "qualified" if qualified else "pending",
            "pending_roles": [] if qualified else pending,
            "missing_baselines": [] if qualified else row["missing_baselines"],
        })
        stages[stage] += 1
        native_counts[row["hop_sequence_id"], "workload"] += 1

    for row in native_report["planned_executions"]:
        hops = [project_issuers(hop) for hop in row["hops"]]
        identifier = hop_execution_id(hops, row["outcome_id"])
        if identifier in seen:
            shared += 1
            continue
        seen.add(identifier)
        if any(hop["operation"] in equivalent_paths for hop in hops):
            stage = "equivalent-support"
        elif hops != row["hops"] or any(hop["operation"] == "acquire" for hop in hops):
            stage = "native-svid"
        else:
            stage = "baseline-issuer"
        report["planned_executions"].append({
            **row, "id": identifier, "hops": hops, "native_stage": stage,
        })
        stages[stage] += 1
        native_counts[row["hop_sequence_id"], "typed"] += 1

    for shape in report["sequences"]:
        key = shape["hop_sequence_id"]
        shape["native_workload_runs"] = native_counts[key, "workload"]
        shape["native_typed_runs"] = native_counts[key, "typed"]
    report["native_operations"] = native_report["operations"]
    report["native_runs_by_stage"] = dict(stages)
    report["shared_native_runs"] = shared
    report["external_total_runs"] = report["total_runs"]
    report["total_runs"] = len(seen)
    report["scenario_definitions"] = list(scenarios.values())
