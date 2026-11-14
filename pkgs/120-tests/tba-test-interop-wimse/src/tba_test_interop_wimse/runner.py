"""Run cases with qualified bindings and an isolated context per execution."""
from dataclasses import asdict

from .observations import mismatches


def run_inventory(scenarios, executions, adapters, *, setup_cache=None):
    cases = {case["id"]: case for case in scenarios}
    setup = {} if setup_cache is None else setup_cache
    for execution in executions:
        case = cases[execution["scenario_id"]]
        result = {"execution_id": execution["id"], "scenario_id": case["id"]}
        adapter = adapters.get(case["scenario_id"])
        if execution["status"] != "qualified":
            gaps = [
                label + ": " + ", ".join(execution[key])
                for key, label in (
                    ("pending_endpoints", "endpoints"),
                    ("missing_baselines", "directional baselines"),
                    ("pending_roles", "support roles"),
                )
                if execution.get(key)
            ]
            reason = "qualification pending" + (" (" + "; ".join(gaps) + ")" if gaps else "")
            yield {**result, "status": "blocked", "reason": reason}
            continue
        if adapter is None or not adapter.supports(case):
            yield {**result, "status": "blocked", "reason": "runtime adapter unavailable"}
            continue
        if hasattr(adapter, "supports_execution") and not adapter.supports_execution(case, execution):
            yield {**result, "status": "blocked", "reason": "adapter does not implement assigned endpoints"}
            continue
        key = (case["scenario_id"], adapter.setup_key(case, execution))
        if key not in setup:
            try:
                adapter.check_setup(case, execution)
            except (AssertionError, OSError, ValueError) as error:
                setup[key] = str(error) or type(error).__name__
            else:
                setup[key] = None
        if setup[key] is not None:
            yield {**result, "status": "setup-failure", "reason": setup[key]}
            continue
        try:
            with adapter.isolated(case, execution) as fixture:
                observed = fixture.observe()
            errors = mismatches(case, observed)
        except (AssertionError, OSError, ValueError) as error:
            yield {**result, "status": "failed", "reason": str(error) or type(error).__name__}
        else:
            yield {**result, "status": "failed" if errors else "passed",
                   "reason": "; ".join(errors), "observation": asdict(observed)}
