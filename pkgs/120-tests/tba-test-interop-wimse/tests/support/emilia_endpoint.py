"""Run the EMILIA provider-entry control in a qualified external workload flow."""

from hashlib import sha256
import json
import subprocess

from support.typed_hop_adapters import observe_http
from support.typed_service_bindings import TypedServiceBindings

OPERATION = "emilia-check"


def bridge_digest(path):
    root = path.parent
    files = (path, root / "package-lock.json", root / "node_modules/@emilia-protocol/gate/dist/index.js")
    return sha256(b"\0".join(file.read_bytes() for file in files)).hexdigest()


def gate_decision(bridge, subject, *, revoke):
    process = subprocess.run(["node", str(bridge)], input=json.dumps({"subject": subject, "revoke": revoke}),
                             text=True, capture_output=True, check=True, timeout=10)
    result = json.loads(process.stdout)
    assert result["reachedEntry"], result
    if revoke:
        assert (result["allow"], result["effects"], result["reason"]) == (
            False, 0, "issuer-revoked-before-effect",
        ), result
        observed = "revocation-before-effect-refused"
    else:
        assert (result["allow"], result["effects"]) == (True, 1), result
        observed = "fresh-authority-accepted-before-effect"
    return {"decision": "allow" if result["allow"] else "deny", "result": observed,
            "gate_observation": result}


class EmiliaBindings(TypedServiceBindings):
    bindings = {**TypedServiceBindings.bindings, OPERATION: {"emilia"}}
    write_gates = {OPERATION}

    def support_request(self, index, fault):
        hop = self.hops[index]
        if hop["operation"] != OPERATION:
            return super().support_request(index, fault)
        bridge = self.agent_factory()
        outcome = observe_http({"subject": hop["caller"]}, lambda request: gate_decision(
            bridge, request["subject"], revoke=fault == "revocation-before-effect-refused",
        ))
        assert outcome.pop("reached_hops") == outcome.pop("decision_hop") == 1
        assert outcome.pop("effects") == 0
        return outcome
