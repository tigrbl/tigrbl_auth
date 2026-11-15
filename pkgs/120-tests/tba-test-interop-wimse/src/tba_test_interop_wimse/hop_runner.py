"""Dispatch typed flow executions and compare observations to the catalog oracle."""


def hop_mismatches(execution, observation):
    expected = {
        "reached_hops": execution["reached_hops"],
        "decision_hop": execution["decision_hop"],
        "result": execution["expected_result"],
        "effects": execution["expected_effects"],
    }
    return [
        f"{field}: expected {value!r}, observed {observation.get(field)!r}"
        for field, value in expected.items() if observation.get(field) != value
    ]


def run_hop_execution(execution, adapters):
    hops = execution["hops"]
    path = tuple(hop["operation"] for hop in hops)
    result = {"execution_id": execution["id"], "hop_sequence_id": execution["hop_sequence_id"]}
    scope = ("native",) if execution.get("native_stage") else ()
    adapter = adapters.get((*scope, *path)) or adapters.get((*scope, "service"))
    # An adapter must inspect the full binding, including endpoint pins and support roles.
    try:
        if adapter is None or not adapter.supports(execution):
            return {**result, "status": "blocked", "reason": "no runtime binding for " + " > ".join(path)}
        observation = adapter.observe(execution)
        errors = hop_mismatches(execution, observation)
    except (AssertionError, KeyError, OSError, ValueError) as error:
        return {**result, "status": "failed", "reason": str(error) or type(error).__name__}
    return {
        **result, "status": "failed" if errors else "passed",
        "reason": "; ".join(errors), "observation": observation,
    }
