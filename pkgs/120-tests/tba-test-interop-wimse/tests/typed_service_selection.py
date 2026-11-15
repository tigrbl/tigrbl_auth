"""Select the typed-service tranche from the agreed expanded inventory."""

from tba_test_interop_wimse.native_expansion import COMBINED_SCOPE, NATIVE_ISSUERS


EXISTING_WORKLOAD_PEERS = {
    "tba", "wimsey", "combined-signature-candidate", "combined-wpt-candidate", "cofide", "cred",
}
SERVICE_OPERATIONS = {
    "check", "call", "delegate", "redeem-delegation", "source-exchange", "destination-exchange",
    "boundary-call", "broker", "provider", "acquire",
}


def typed_service_rows(plan):
    selected = []
    for row in plan["planned_executions"]:
        hops = row["hops"]
        path = tuple(hop["operation"] for hop in hops)
        if path in {("delegate",), ("check",), ("call",) * 3} or set(path) - SERVICE_OPERATIONS:
            continue
        if row.get("native_stage") == "equivalent-support" or (
            "acquire" in path and row.get("native_stage")
        ):
            continue
        if any(hop[key][0] not in EXISTING_WORKLOAD_PEERS
               for hop in hops for key in ("caller_pin", "receiver_pin") if key in hop):
            continue
        selected.append(row)
    return selected


def native_acquisition_rows(plan, *, specialized=False):
    stage = "equivalent-support" if specialized else "native-svid"
    return [
        row for row in plan["planned_executions"]
        if row.get("native_stage") == stage
        and row["hops"][0].get("support") == "planned-tba-workload-api"
    ]


def native_baseline_policy_case(row):
    return row.get("native_stage") == "equivalent-support" and all(
        hop.get(field, "none") in {"none", "baseline"}
        for hop in row["hops"] for field in ("wic_issuer", "wit_issuer")
    )


def native_baseline_policy_rows(plan):
    return [row for row in plan["planned_executions"] if native_baseline_policy_case(row)]


def policy_svid_scope(row):
    issuers = {
        hop.get(field) for hop in row["hops"] for field in ("wic_issuer", "wit_issuer")
    } & NATIVE_ISSUERS.keys()
    return COMBINED_SCOPE if len(issuers) == 2 else next(iter(issuers), None)


def native_svid_policy_case(row):
    return (
        row.get("native_stage") == "equivalent-support"
        and row["hops"][0].get("support") != "planned-tba-workload-api"
        and policy_svid_scope(row) is not None
    )


def native_svid_policy_rows(plan):
    return [row for row in plan["planned_executions"] if native_svid_policy_case(row)]


def svid_policy_control_rows(rows):
    choices = {}
    for row in rows:
        hops = row["hops"]
        path = tuple(hop["operation"] for hop in hops)
        key = policy_svid_scope(row), path, row["outcome_id"]
        choices.setdefault(key, row)
    return list(choices.values())


def acquisition_control_rows(rows, *, specialized=False):
    choices = {}
    for row in rows:
        hops = row["hops"]
        path = tuple(hop["operation"] for hop in hops)
        next_profile = (hops[1]["profile"], hops[1]["wit_issuer"]) if len(hops) > 1 else ()
        if specialized and row["outcome_id"] != "success":
            next_profile = ()
        choices.setdefault((path, next_profile, row["outcome_id"]), row)
    return list(choices.values())


def service_control_rows(rows):
    choices = {}
    for row in rows:
        path = tuple(hop["operation"] for hop in row["hops"])
        key = bool(row.get("native_stage")), path, row["outcome_id"]
        choices.setdefault(key, row)
    # Prove status placement first, then the other support bindings.
    keys = sorted(choices, key=lambda key: (bool(set(key[1]) - {"call", "check"}), key))
    return [choices[key] for key in keys]
