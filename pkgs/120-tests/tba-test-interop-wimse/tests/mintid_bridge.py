"""Run one live MintID status decision inside the pinned test stack."""

from argparse import Namespace
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import sys

from revocation_trace import (
    Stack, Trace, baseline, baseline_budget, mint_agent, onboard_principal,
    path_issuer, path_kill_switch, wait_ready,
)


def observe(path, actor, trace_dir):
    stack = Stack(Namespace(target="local"))
    stack.custody_floor = None
    trace = Trace(Path(trace_dir), "local")
    principal = onboard_principal(stack, trace, actor)
    agent_role = "kill" if path == "kill_switch" else "issuer"
    agents = {agent_role: mint_agent(principal)}
    if path == "issuer":
        agents["sibling"] = mint_agent(principal)
    wait_ready(stack, trace, list(agents.values()), stack.issuer_info()["status_epoch"])
    status = stack.status_view()
    self_revocation = stack.issuer_info().get("selfrevoke") or {}
    fixture = {"agents": agents, "A": status["max_root_age_seconds"], "H": status["heartbeat_seconds"],
               "K": 5, "G": int(self_revocation.get("fold_grace_seconds") or 60)}
    if not path:
        accepted, _ = baseline(stack, trace, "issuer", "active",
                               fixture["agents"]["issuer"], baseline_budget(fixture))
        if not accepted or not accepted["accepted"]:
            raise ValueError("MintID verifier never accepted the fresh credential")
        return {"accepted": True, "actor": actor, "reason": accepted["reason_code"],
                "session_id": accepted["session_id"]}
    result = {"issuer": path_issuer, "kill_switch": path_kill_switch}[path](stack, trace, fixture)
    refusal = result.get("first_no")
    if (not refusal or not result["baseline"]["accepted"] or refusal["accepted"]
            or not refusal.get("confirmed_by") or not result.get("refresh_failed_at")
            or not result.get("carrying_root")):
        raise ValueError("MintID did not attribute a verifier refusal to the requested revocation")
    return {"accepted": False, "actor": actor, "reason": refusal["reason_code"], "session_id": refusal["session_id"],
            "revocation_path": path, "refusal_confirmed": True, "witness_refresh_refused": True}


if __name__ == "__main__":
    request = json.load(sys.stdin)
    with TemporaryDirectory() as directory, redirect_stdout(sys.stderr):
        result = observe(request["path"], request["actor"], directory)
    print(json.dumps(result))
