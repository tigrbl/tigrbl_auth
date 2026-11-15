from collections import Counter

from tba_test_interop_wimse.catalog import read_catalog
from tba_test_interop_wimse.hop_expansion import include_candidate_endpoints, plan_hop_expansion
from tba_test_interop_wimse.hop_matrix import generate_hop_matrix
from tba_test_interop_wimse.matrix import generate_matrix
from tba_test_interop_wimse.native_expansion import (
    COMBINED_RECORD, COMBINED_SCOPE, expanded_plan, native_issuer_rows, native_operation_catalog,
)


def test_entity_roles_agree_with_peer_bindings():
    hops = read_catalog("hops.toml")
    peers = read_catalog("peers.toml")
    roles = hops["entity_roles"]
    types = hops["entity_types"]
    implementations = peers["implementations"]
    support = peers["lab_support_bindings"]

    assert set(roles.values()) <= types.keys()
    for implementation in implementations.values():
        assert implementation["entity_types"]
        assert set(implementation["entity_types"]) <= types.keys()
        for role in implementation.get("candidate_support_roles", ()):
            assert roles[role] in implementation["entity_types"]
        if implementation.get("candidate_endpoint_profiles"):
            assert "workload" in implementation["entity_types"]
    tba = implementations["tba"]
    native_roles = tba["native_roles"]
    assert native_roles.keys() == roles.keys()
    assert set(native_roles.values()) <= {"interop-qualified", "local-fixture", "components", "planned"}
    for role, readiness in native_roles.items():
        entity_type = roles[role]
        if entity_type in tba["planned_entity_types"]:
            assert readiness in {"components", "planned"}
        else:
            assert entity_type in tba["entity_types"]
    for binding in support.values():
        assert binding["role"] in roles
        if implementation := binding.get("implementation"):
            entity_type = roles[binding["role"]]
            peer = implementations[implementation]
            assert entity_type in peer["entity_types"] or (
                binding["status"] == "planned" and entity_type in peer["planned_entity_types"]
            )
    for capability in peers["capabilities"]:
        assert roles[capability["role"]] in implementations[capability["implementation"]]["entity_types"]

    for operation in hops["operations"].values():
        assert roles[operation["source_role"]] == "workload"
        destination = operation["destination_role"]
        assert destination in roles
        if operation.get("advances_actor"):
            assert roles[destination] == "workload"
        if "candidate" in operation:
            assert operation["candidate_role"] == destination
            assert destination in implementations[operation["candidate"]]["candidate_support_roles"]
        elif "support" in operation:
            binding = support[operation["support"]]
            assert binding["role"] == operation.get("support_role", destination)


def test_native_projection_keeps_existing_ids_and_validates_native_roles():
    peers = read_catalog("peers.toml")
    external = expanded_plan(peers, include_candidates=True, include_executions=True)
    full = expanded_plan(peers, include_candidates=True, include_native=True, include_executions=True)
    groups = ("workload_executions", "planned_executions")
    for group in groups:
        assert full[group][:len(external[group])] == external[group]
    rows = [row for group in groups for row in full[group]]
    assert len({row["id"] for row in rows}) == len(rows) == full["total_runs"]
    assert sum(full["native_runs_by_stage"].values()) == full["total_runs"] - external["total_runs"]
    native_workloads = [row for row in full["workload_executions"] if "native_stage" in row]
    assert {row["status"] for row in native_workloads} == {"pending"}
    assert all(
        endpoint["implementation"] == "tba" for row in native_workloads
        for pair in row["pairs"].values() for endpoint in pair.values()
    )
    for row in full["planned_executions"]:
        if "native_stage" in row:
            assert not any(hop.get("wic_issuer") == "spire-x509-svid" or
                           hop.get("wit_issuer") == "spire-wit-svid" for hop in row["hops"])
    catalog = native_operation_catalog()
    native = catalog["native"]
    names = set(native["overrides"]) | {item["operation"] for item in native["equivalent_operations"].values()}
    for name in names:
        operation = catalog["operations"][name]
        if "support" in operation:
            binding = peers["lab_support_bindings"][operation["support"]]
            assert binding["implementation"] == "tba"
            assert binding["role"] == operation["destination_role"]


def test_hop_inventory_accounts_for_existing_scenarios_and_runs():
    matrix = generate_matrix()
    rows = generate_hop_matrix(matrix)["sequences"]
    assert len({row["hop_sequence_id"] for row in rows}) == 155
    assert Counter(row["hop_count"] for row in rows) == {1: 5, 2: 25, 3: 125}
    by_id = {row["hop_sequence_id"]: row for row in rows}
    assert by_id["workload-call"]["candidate_runs"] == 992
    assert by_id["workload-call+workload-call"]["candidate_runs"] == 3462
    assert sum(row["candidate_runs"] for row in rows) == len(matrix["executions"])
    assert sum(row["structural_scenarios"] for row in rows) == len(matrix["scenarios"])
    assert by_id["workload-call+workload-call+workload-call"]["status"] == "proposed"
    assert by_id["delegation+token-exchange+workload-call"]["candidate_runs"] == 0
    assert len(by_id["delegation+token-exchange+workload-call"]["binding_gaps"]) == 3
    assert by_id["workload-call"]["binding_gaps"] == []


def test_individual_issuer_controls_do_not_qualify_combined_workloads():
    peers = read_catalog("peers.toml")
    version = "native-qualification-test"
    configuration = "native-qualification-test"
    for capability in peers["capabilities"]:
        if capability["implementation"] == "tba":
            capability.update(version=version, configuration=configuration,
                              status="qualified", evidence="test endpoint controls")
    common_profiles = [("wic-mtls-wpt", "spiffe"), ("wic-mtls-http-signature", "spiffe")]
    for key in ("native_wit_svid", "native_x509_svid"):
        peers[key] = {"version": version, "profiles": common_profiles, "evidence": "component controls"}

    def direct_controls():
        plan = expanded_plan(peers, include_native=True, include_executions=True)
        workloads, _ = native_issuer_rows(plan, COMBINED_SCOPE)
        return {row["id"]: row["status"] for row in workloads if row["scenario_id"].startswith("01:")}

    pending = direct_controls()
    assert len(pending) == 2 and set(pending.values()) == {"pending"}
    peers[COMBINED_RECORD] = {"version": version, "profiles": common_profiles, "evidence": "combined controls"}
    qualified = direct_controls()
    assert qualified.keys() == pending.keys()
    assert set(qualified.values()) == {"qualified"}


def test_hop_expansion_binds_inputs_and_deduplicates_new_ids():
    peers = read_catalog("peers.toml")
    baseline = generate_matrix(peers=peers)
    report = plan_hop_expansion(baseline, peers, include_executions=True)
    planned = report["planned_executions"]
    by_sequence = {s["hop_sequence_id"]: s for s in report["sequences"]}
    assert len(by_sequence) == 155
    ids = {row["id"] for row in planned}
    assert len(ids) == len(planned) == sum(row["new_planned_runs"] for row in by_sequence.values())
    assert not ids.intersection(row["id"] for row in baseline["executions"])
    assert report["total_runs"] == report["existing_runs"] + len(ids)
    assert by_sequence["token-exchange+credential-acquisition"]["new_planned_runs"] == 0

    for row in planned:
        hops = row["hops"]
        if hops[0]["operation"] == "acquire" and len(hops) > 1:
            assert hops[0]["caller_pin"] == hops[1]["caller_pin"]
            assert hops[1]["wic_issuer"] == "spire-x509-svid"
        if hops[-1]["operation"] == "provider":
            assert hops[-1]["caller_pin"] == hops[-2]["receiver_pin"]
            assert hops[-1]["caller_pin"][0] == "cred"
        if row["outcome_id"] != "success":
            assert row["expected_effects"] == 0
            assert row["reached_hops"] == row["decision_hop"] <= len(hops)


def test_candidate_expansion_preserves_ids_and_respects_peer_roles():
    peers = read_catalog("peers.toml")
    baseline = generate_matrix(peers=peers)
    existing = plan_hop_expansion(baseline, peers, include_executions=True)
    expanded_peers = include_candidate_endpoints(peers)
    expanded_matrix = generate_matrix(peers=expanded_peers)
    report = plan_hop_expansion(
        expanded_matrix, expanded_peers, include_executions=True, include_candidates=True,
    )
    workload = {row["id"]: row for row in report["workload_executions"]}
    original = {row["id"]: row for row in baseline["executions"]}
    assert all(workload[key] == row for key, row in original.items())
    assert {row["status"] for key, row in workload.items()
            if key not in original} == {"pending"}
    planned = {row["id"]: row for row in report["planned_executions"]}
    assert all(planned[row["id"]] == row for row in existing["planned_executions"])
    assert len(workload.keys() | planned.keys()) == report["total_runs"]
    counts = Counter()
    for row in planned.values():
        for hop in row["hops"]:
            if "support" in hop:
                counts[hop["support"]] += 1
    assert {"authgent", "emilia", "mintid", "omniarx", "redthread", "teleport-tbot"} <= counts.keys()
