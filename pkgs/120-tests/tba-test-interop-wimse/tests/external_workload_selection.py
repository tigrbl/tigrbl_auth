"""Select the pinned SPIFFE peer flows without unqualified support roles."""

from hashlib import sha256

from tba_test_interop_wimse.catalog import read_catalog


CANDIDATES = frozenset({"go-spiffe", "defakto", "agentmaurice"})
DEPENDENCIES = frozenset(
    name for name, row in read_catalog("peers.toml")["implementations"].items()
    if row.get("candidate_support_roles")
)


def endpoint_candidates(row):
    names = {endpoint["implementation"] for pair in row.get("pairs", {}).values() for endpoint in pair.values()}
    names.update(pin[0] for hop in row.get("hops", ()) for key, pin in hop.items() if key.endswith("_pin"))
    return names & CANDIDATES


def spiffe_peer_rows(plan, *, defakto=False):
    candidate_sets = ({"defakto"}, {"defakto", "go-spiffe"}) if defakto else ({"go-spiffe"},)
    workload = [row for row in plan["workload_executions"] if endpoint_candidates(row) in candidate_sets]
    typed = [row for row in plan["planned_executions"] if endpoint_candidates(row) in candidate_sets
             and not any(hop.get("support") in DEPENDENCIES for hop in row["hops"])]
    return workload, typed


def spiffe_emilia_rows(plan):
    return spiffe_support_rows(plan, "emilia")


def spiffe_support_rows(plan, support):
    return [
        row for row in plan["planned_executions"]
        if endpoint_candidates(row) in ({"go-spiffe"}, {"defakto"})
        and any(hop.get("support") == support for hop in row["hops"])
    ]


def defakto_digest(bridge):
    root = bridge.parent
    files = (bridge, root / "package-lock.json", root / "node_modules/@defakto/spiffe/dist/index.js")
    return sha256(b"\0".join(path.read_bytes() for path in files)).hexdigest()
