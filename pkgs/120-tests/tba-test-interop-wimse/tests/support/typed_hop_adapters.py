"""Local loopback adapters for standalone status and delegation flows."""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from threading import Thread
from urllib.request import Request, urlopen

from support.wic_policy import CHILD, STATUS_INPUTS, status_evidence, validate_child
from support.wic_services import TokenIssuer


def observe_http(payload, evaluate, *, headers=None):
    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            request = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            trace["reached_hops"] += 1
            result = evaluate(request) if headers is None else evaluate(request, self.headers)
            body = json.dumps(result).encode()
            trace["decision_hop"] = trace["reached_hops"]
            self.send_response(200)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args):
            pass

    trace = {"reached_hops": 0, "decision_hop": 0, "effects": 0}
    with HTTPServer(("127.0.0.1", 0), Handler) as server:
        worker = Thread(target=server.serve_forever, kwargs={"poll_interval": 0.01}, daemon=True)
        worker.start()
        try:
            request = Request(
                f"http://127.0.0.1:{server.server_port}/", data=json.dumps(payload).encode(),
                headers={"Content-Type": "application/json", **(headers or {})},
            )
            with urlopen(request, timeout=5) as response:
                observed = json.load(response)
        finally:
            server.shutdown()
            worker.join()
    return {**trace, **observed}


class LocalStatusAdapter:
    outcomes = {
        "success": "current-status",
        "1:revoked-status-refused": "confirmed-revoked",
        "1:stale-status-refused": "stale-cache",
        "1:unavailable-status-refused": "unavailable-status",
    }

    def supports(self, execution):
        hop, = execution["hops"]
        return (hop["support"] == "status-authority"
                and tuple(hop["caller_pin"]) == ("tba", None, "planned-lab-fixture")
                and execution["outcome_id"] in self.outcomes)

    def observe(self, execution):
        evidence, grace, _ = STATUS_INPUTS[self.outcomes[execution["outcome_id"]]]

        def evaluate(request):
            try:
                status_evidence(request["evidence"], grace=grace)
            except ValueError as error:
                result = {
                    "delegated-status-revoked": "revoked-status-refused",
                    "delegated-status-stale": "stale-status-refused",
                    "delegated-status-unavailable": "unavailable-status-refused",
                }[str(error)]
            else:
                result = "fresh-status-accepted"
            return {"result": result}

        return observe_http({"evidence": evidence}, evaluate)


class LocalDelegationAdapter:
    def supports(self, execution):
        hop, = execution["hops"]
        local = ("tba", None, "planned-lab-fixture")
        return (hop["support"] == "lab-delegation-authority"
                and tuple(hop["caller_pin"]) == tuple(hop["receiver_pin"]) == local
                and execution["outcome_id"] in {"success", "1:delegation-widens-parent-scope"})

    def observe(self, execution):
        issuer = TokenIssuer("local-parent", "local-delegate")
        proposed = dict(CHILD)
        if execution["outcome_id"] == "1:delegation-widens-parent-scope":
            proposed["methods"] = ["DELETE"]

        def evaluate(request):
            try:
                validate_child(request)
            except ValueError as error:
                if str(error) != "child-method-outside-parent":
                    raise
                return {"result": "delegation-widens-parent-scope"}
            token = issuer.issue("local-delegate", ",".join(request["methods"]))
            return {"grant": token}

        observed = observe_http(proposed, evaluate)
        if "grant" in observed:
            claims = issuer.verify(observed.pop("grant"))
            assert claims["sub"] == "local-delegate" and claims["scope"] == "POST"
            observed["result"] = "narrowed-authority-issued"
        return observed
