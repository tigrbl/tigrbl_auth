"""Plan typed lab flows using operation contracts and endpoint capabilities."""

from collections import Counter
from copy import deepcopy
from hashlib import sha256
from itertools import product
import json

from .catalog import read_catalog
from .hop_matrix import generate_hop_matrix
from .matrix import endpoint_pairs, profile_options


def include_candidate_endpoints(peers):
    """Keep the qualified snapshot and overlay catalog proposals as pending endpoints."""
    expanded = deepcopy(peers)
    implementations = read_catalog("peers.toml")["implementations"]
    for name, candidate in implementations.items():
        profiles = candidate.get("candidate_endpoint_profiles", [])
        if not profiles:
            continue
        expanded["implementations"].setdefault(name, candidate)
        for profile in profiles:
            for role in profile["roles"]:
                capability = {
                    "implementation": name, "role": role, "profile": profile["profile"],
                    "identifier_scheme": profile["identifier_scheme"], "status": "pending",
                }
                match = {key: value for key, value in capability.items() if key != "status"}
                if not any(all(row.get(key) == value for key, value in match.items())
                           for row in expanded["capabilities"]):
                    expanded["capabilities"].append(capability)
    return expanded


def operation_paths(sequence, operations):
    by_type = [
        [name for name, operation in operations.items() if operation["type"] == kind]
        for kind in sequence
    ]
    for path in product(*by_type):
        if "initial_input" not in operations[path[0]]:
            continue
        if not operations[path[-1]].get("terminal", True):
            continue
        if all(right in operations[left]["next"] for left, right in zip(path, path[1:])):
            yield path


def endpoint_key(endpoint):
    return tuple(endpoint.get(field) for field in ("implementation", "version", "configuration"))


def call_options(profiles, peers, operation, requirement, *, native_only=False):
    for profile in profiles:
        if requirement == "application-proof" and profile["application_proof"] == "None":
            continue
        if requirement == "spire-x509-svid" and profile["wic_issuer"] != requirement:
            continue
        for pair in endpoint_pairs(peers, profile, native_only=native_only):
            receiver = operation.get("receiver")
            if receiver and pair["receiver"]["implementation"] != receiver:
                continue
            yield {
                "caller_pin": endpoint_key(pair["caller"]),
                "receiver_pin": endpoint_key(pair["receiver"]),
                "profile": profile["profile"],
                "identifier_scheme": profile["identifier_scheme"],
                "wic_issuer": profile["wic_issuer"],
                "wit_issuer": profile["wit_issuer"],
            }


def bind_path(path, operations, options):
    actor = 0
    hops = []
    choices = []
    for index, name in enumerate(path):
        operation = operations[name]
        hop = {"operation": name, "type": operation["type"], "caller": f"workload-{actor}"}
        if operation.get("advances_actor"):
            actor += 1
            hop["receiver"] = f"workload-{actor}"
        if "support" in operation:
            hop["support"] = operation["support"]
            hop.setdefault("receiver", operation["support"])
        else:
            predecessor = operations[path[index - 1]] if index else {}
            requirement = operation.get("profile_requirement") or predecessor.get("following_call")
            choices.append((
                index,
                [
                    {**call, "wic_issuer": predecessor.get("following_issuer", call["wic_issuer"])}
                    for call in options[name, requirement]
                    if (
                        predecessor.get("following_profile") != "wit-proof"
                        or call["profile"] in {"wit-wpt", "wit-http-signature"}
                    ) and predecessor.get("following_receiver", call["receiver_pin"][0]) == call["receiver_pin"][0]
                ],
            ))
        hops.append(hop)

    for selected in product(*(items for _, items in choices)):
        pins = {}
        bound = [hop.copy() for hop in hops]
        for (index, _), call in zip(choices, selected):
            hop = bound[index]
            assignments = ((hop["caller"], call["caller_pin"]), (hop["receiver"], call["receiver_pin"]))
            if any(role in pins and pins[role] != pin for role, pin in assignments):
                break
            pins.update(assignments)
            hop.update(call)
        else:
            if any(
                pins.get(hop[side], ("tba",))[0] != operation[f"{side}_implementation"]
                for name, hop in zip(path, bound)
                for operation in (operations[name],)
                for side in ("caller", "receiver")
                if f"{side}_implementation" in operation
            ):
                continue
            for hop in bound:
                for side in ("caller", "receiver"):
                    role = hop[side]
                    if role.startswith("workload-"):
                        hop[f"{side}_pin"] = pins.get(role, ("tba", None, "planned-lab-fixture"))
            yield bound


def outcomes(path, operations):
    # Effects are delayed until the whole chain authorizes the operation.
    final = operations[path[-1]]
    effectful = "provider" in path or (
        "call" in path and (path[-1] in {"call", "check"} or final.get("gates_effect"))
    )
    yield {
        "outcome_id": "success",
        "reached_hops": len(path),
        "decision_hop": len(path),
        "expected_result": operations[path[-1]]["success"],
        "expected_effects": int(effectful),
    }
    for index, name in enumerate(path, start=1):
        for refusal in operations[name]["refusals"]:
            yield {
                "outcome_id": f"{index}:{refusal}",
                "reached_hops": index,
                "decision_hop": index,
                "expected_result": refusal,
                "expected_effects": 0,
            }


def hop_execution_id(hops, outcome_id):
    canonical = json.dumps([hops, outcome_id], sort_keys=True, separators=(",", ":"))
    return "hop-v1:" + sha256(canonical.encode()).hexdigest()


def plan_hop_expansion(matrix, peers, *, include_executions=False, include_candidates=False,
                       native_only=False, catalog=None):
    report = generate_hop_matrix(matrix)
    catalog = read_catalog("hops.toml") if catalog is None else catalog
    all_operations = catalog["operations"]
    if any(set(op["next"]) - all_operations.keys() for op in all_operations.values()):
        raise ValueError("An operation allows an unknown following operation")
    implementations = read_catalog("peers.toml")["implementations"]
    operations = {}
    for name, operation in all_operations.items():
        candidate = operation.get("candidate")
        if candidate is None:
            operations[name] = operation
        elif include_candidates:
            if operation["candidate_role"] not in implementations[candidate]["candidate_support_roles"]:
                raise ValueError(f"{candidate} does not declare the support role for {name}")
            operations[name] = operation
    factors = read_catalog("factors.toml")
    profiles = list(profile_options(factors["hop_profiles"], factors))
    requirements = {None, *(op["following_call"] for op in operations.values() if "following_call" in op),
                    *(op["profile_requirement"] for op in operations.values() if "profile_requirement" in op)}
    if requirements - {None, "application-proof", "spire-x509-svid"}:
        raise ValueError("Unknown workload profile requirement")
    options = {
        (name, requirement): list(call_options(profiles, peers, op, requirement, native_only=native_only))
        for name, op in operations.items() if "support" not in op
        for requirement in requirements
    }
    existing_ids = {row["id"] for row in matrix["executions"]}
    planned_ids = set()
    planned = []
    for shape in report["sequences"]:
        counts = Counter()
        flow_paths = []
        for path in operation_paths(shape["hop_types"], operations):
            if shape["candidate_runs"] and set(path) == {"call"}:
                continue  # The existing scenario catalog already owns this generic workload flow.
            counts["flows"] += 1
            flow_paths.append(path)
            expected_outcomes = list(outcomes(path, operations))
            for hops in bind_path(path, operations, options):
                counts["assignments"] += 1
                for outcome in expected_outcomes:
                    run_id = hop_execution_id(hops, outcome["outcome_id"])
                    if run_id in planned_ids or run_id in existing_ids:
                        continue
                    planned_ids.add(run_id)
                    counts["runs"] += 1
                    if include_executions:
                        planned.append({
                            "id": run_id,
                            "status": "planned",
                            "hop_sequence_id": shape["hop_sequence_id"],
                            "initial_input": operations[path[0]]["initial_input"],
                            "hops": hops,
                            **outcome,
                        })
        shape.update(
            admitted_flows=flow_paths,
            compatible_assignments=counts["assignments"],
            new_planned_runs=counts["runs"],
        )
        if counts["runs"]:
            shape["disposition"] = "expanded"
            shape["binding_gaps"] = []
        elif shape["candidate_runs"]:
            shape["disposition"] = "existing"
        elif counts["flows"]:
            shape["disposition"] = "no-compatible-endpoint-assignment"
        else:
            shape["disposition"] = "no-complete-flow-in-current-contracts"
    report["operations"] = operations
    report["existing_runs"] = len(existing_ids)
    report["new_planned_runs"] = len(planned_ids)
    report["total_runs"] = len(existing_ids) + len(planned_ids)
    if include_executions:
        report["workload_executions"] = matrix["executions"]
        report["planned_executions"] = planned
    return report
