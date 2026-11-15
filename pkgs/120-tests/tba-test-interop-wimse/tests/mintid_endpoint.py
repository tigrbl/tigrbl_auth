"""Use the MintID verifier at the final policy hop before writing an effect."""

from pathlib import Path
import json
import subprocess

from support.typed_service_bindings import TypedServiceBindings


OPERATION = "mintid-check"
BRIDGE = Path(__file__).with_name("mintid_bridge.py")
RUNTIME_BRIDGE = "/tbafixture/mintid_bridge.py"
DECISION_TIMEOUT = 480
REVOCATIONS = {
    "issuer-revocation-refused": "issuer",
    "holder-self-revocation-refused": "kill_switch",
}


class MintIDBindings(TypedServiceBindings):
    bindings = {**TypedServiceBindings.bindings, OPERATION: {"mintid"}}
    write_gates = {OPERATION}

    def support_request(self, index, fault):
        if self.hops[index]["operation"] != OPERATION:
            return super().support_request(index, fault)
        path = REVOCATIONS[fault] if fault else ""
        actor = self.hops[index]["caller"]
        try:
            reply = subprocess.run(
                ["docker", "exec", "-i", self.agent_factory(), "python", RUNTIME_BRIDGE],
                input=json.dumps({"path": path, "actor": actor}), text=True, capture_output=True,
                timeout=DECISION_TIMEOUT, check=True,
            )
        except subprocess.CalledProcessError as error:
            raise ValueError("MintID trace did not produce an attributable decision") from error
        except subprocess.TimeoutExpired as error:
            raise ValueError("MintID trace exceeded its runtime budget") from error
        result = json.loads(reply.stdout)
        if not result.get("session_id") or result.get("actor") != actor:
            raise ValueError("MintID trace omitted the verifier session or workload mapping")
        if path:
            if (result.get("revocation_path") != path or result.get("accepted") is not False
                    or not result.get("refusal_confirmed") or not result.get("witness_refresh_refused")):
                raise ValueError("MintID verifier did not confirm the requested revocation")
            return {**self.refusal(fault), "mintid_verifier": result}
        if result.get("accepted") is not True:
            raise ValueError("MintID verifier refused the active credential")
        return self.accepted("current-non-revocation-proof-accepted", mintid_verifier=result)
