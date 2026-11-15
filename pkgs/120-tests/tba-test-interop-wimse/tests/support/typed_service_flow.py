"""Run a typed service flow with live workload and support requests."""

from contextlib import ExitStack
from dataclasses import replace
from hashlib import sha256

from tba_test_interop_wimse.native_expansion import COMBINED_SCOPE, matches_native_issuer_scope

from support.signature_cases import SignatureHop
from support.typed_hop_adapters import LocalStatusAdapter, observe_http
from support.typed_workload_chain import native_workload_hop
from support.wic_policy import STATUS_INPUTS, status_evidence
from support.wic_support_cases import request
from support.wpt_fixture import WptFixture


WORKLOAD_OPERATIONS = {"call", "boundary-call", "broker"}
ACQUISITION_OPERATIONS = {"acquire", "teleport-acquire"}
DOWNSTREAM_REFUSAL = "typed-downstream-refused"


class StatusFlowServices:
    bindings = {"check": {"status-authority"}}
    write_gates = ()

    def __init__(self, hops, agent_factory=None):
        self.hops = hops
        self.effects = 0

    def headers(self, index, fault, fixture):
        return {}

    def workload_evidence(self, index):
        return {}

    def authorize(self, index, identity, headers, fault, fixture):
        if fault == "operation-scope-refused":
            raise ValueError("operation-scope-refused")

    def support_request(self, index, fault):
        hop = self.hops[index]
        outcome = f"1:{fault}" if fault else "success"
        evidence, grace, _ = STATUS_INPUTS[LocalStatusAdapter.outcomes[outcome]]
        # Keep the status at the authority. The verifier asks about a
        # participant and only receives the authority's decision.
        def evaluate(payload):
            assert payload["subject"] == hop["caller"]
            try:
                status_evidence(evidence, grace=grace)
            except ValueError as error:
                reason = {
                    "delegated-status-revoked": "revoked-status-refused",
                    "delegated-status-stale": "stale-status-refused",
                    "delegated-status-unavailable": "unavailable-status-refused",
                }[str(error)]
                return {"decision": "deny", "result": reason}
            return {"decision": "allow", "result": "fresh-status-accepted"}

        result = observe_http({"subject": hop["caller"]}, evaluate)
        assert result["reached_hops"] == 1 and result["decision_hop"] == 1
        return {"decision": result["decision"], "result": result["result"]}

    def configure_lab(self, lab):
        return lab


class TypedServiceFlow:
    def __init__(self, workload_chain, services=StatusFlowServices, *, agent_factory=None, record_svids=False,
                 workload_response_timeout=None):
        self.workload_chain = workload_chain
        self.services = services
        self.agent_factory = agent_factory
        self.record_svids = record_svids
        self.workload_response_timeout = workload_response_timeout

    def supports(self, execution):
        hops = execution["hops"]
        if any(hop["operation"] in ACQUISITION_OPERATIONS for hop in hops) and self.agent_factory is None:
            return False
        if any(hop["operation"] not in WORKLOAD_OPERATIONS
               and hop.get("support") not in self.services.bindings.get(hop["operation"], ())
               for hop in hops):
            return False
        workload = [hop for hop in hops if hop["operation"] in WORKLOAD_OPERATIONS]
        chain = self.workload_chain
        if (chain.native_directory is not None and not chain.native_combined_svid
                and matches_native_issuer_scope(workload, COMBINED_SCOPE)):
            return False
        return chain.supports({"hops": workload})

    def observe(self, execution):
        hops = execution["hops"]
        target, _, requested_fault = execution["outcome_id"].partition(":")
        operations = [hop["operation"] for hop in hops]
        calls = [index for index, operation in enumerate(operations) if operation in WORKLOAD_OPERATIONS]
        write_index = calls[-1] if calls and (
            operations[-1] in {"call", "check"} or operations[-1] in self.services.write_gates
        ) else None
        services = self.services(hops, self.agent_factory)
        chain = self.workload_chain
        trace = []
        endpoints = {}
        admitted = set()
        presented = []
        credentials = {}

        def fault_at(index):
            return requested_fault if str(index + 1) == target else ""

        def invoke(index):
            if index == len(hops):
                return True
            operation = operations[index]
            record = {"hop": index + 1, "operation": operation, "participant": hops[index]["receiver"]}
            trace.append(record)
            if index not in endpoints:
                record.update(services.support_request(index, fault_at(index)))
                return record["decision"] == "allow" and invoke(index + 1)
            fixture, endpoint = endpoints[index]
            reply = request(endpoint, read=index != write_index, **services.headers(index, fault_at(index), fixture))
            body = reply["response"]
            record.update(http_status=reply["http_status"], decision=body["decision"])
            if credentials.get(index):
                record["svids"] = credentials[index]
            record.update(services.workload_evidence(index))
            if body["decision"] == "allow":
                assert reply["http_status"] == (201 if index == write_index else 200), reply
                record["result"] = workload_success[operation]
                return True
            assert body["decision"] == "deny" and reply["http_status"] in {401, 403}, reply
            reason = body.get("reason", "")
            record["reason"] = reason
            if reason == DOWNSTREAM_REFUSAL:
                assert index in admitted and trace[-1] is not record
                record["result"] = workload_success[operation]
            elif reason in workload_refusals:
                record["result"] = reason
            else:
                assert index not in admitted
                record["result"] = "peer-identity-refused"
            return False

        workload_success = {
            "call": "operation-authorized",
            "boundary-call": "cross-domain-worker-admitted",
            "broker": "broker-authorized-credential-use",
        }
        workload_refusals = {
            "operation-scope-refused", "foreign-domain-token-refused",
            "broker-grant-refused", "revocation-before-provider-call",
        }
        start = 0
        if operations[0] in ACQUISITION_OPERATIONS:
            acquisition = services.support_request(0, fault_at(0))
            trace.append({"hop": 1, "operation": operations[0], "participant": hops[0]["receiver"], **acquisition})
            if acquisition["decision"] == "deny" or len(hops) == 1:
                return {"reached_hops": 1, "decision_hop": 1, "result": acquisition["result"],
                        "effects": 0, "trace": trace}
            start = 1
        lab = services.configure_lab(chain.get_lab().signature) if chain.get_lab and calls else None
        with ExitStack() as stack:
            for index in reversed(calls):
                hop = hops[index]
                wrong_identity = fault_at(index) == "peer-identity-refused"
                transport_fault = wrong_identity and hop["profile"] == "wic-mtls"
                name = str(index + 1)
                case = {
                    "scenario_id": "01", "variant": "wrong-anchor" if transport_fault else "valid-peer",
                    "layer": "tls" if transport_fault else "operation", "hops": {name: hop}, "target_hop": name,
                }
                direction = "forward" if hop["caller_pin"][0] == "tba" else "reverse"
                names = {"caller_name": hop["caller"], "receiver_name": hop["receiver"]}
                if chain.native_directory is None:
                    binding = lab.hop(case, direction, hop, names)
                else:
                    acquired = services.acquired_issuer if start and index == start else None
                    binding = native_workload_hop(
                        chain.native_directory, case, hop, names, acquired=acquired,
                        presented=presented.append if acquired is not None else None,
                    )
                fixture = stack.enter_context(binding)
                if index == start and operations[0] == "teleport-acquire":
                    verify = fixture.receiver_verifier.verify

                    def record_peer_certificate(certificate, **kwargs):
                        presented.append(certificate)
                        return verify(certificate, **kwargs)

                    fixture.receiver_verifier.verify = record_peer_certificate
                if isinstance(fixture, WptFixture):
                    variant = "wrong-anchor" if wrong_identity else "valid-peer"
                    fixture = SignatureHop(
                        fixture, operation_variant=variant if index == write_index else "valid-peer",
                        read_variant=variant if index != write_index else "valid-peer",
                    )

                def authorize(identity, headers, *, current=index, receiver=fixture):
                    assert identity == receiver.identity
                    services.authorize(current, identity, headers, fault_at(current), receiver)
                    admitted.add(current)
                    if not invoke(current + 1):
                        raise ValueError(DOWNSTREAM_REFUSAL)
                    return {}

                endpoint = stack.enter_context(fixture.running(
                    authorize_write=authorize if index == write_index else None,
                    authorize_read=authorize if index != write_index else None,
                ))
                if self.workload_response_timeout is not None:
                    caller, receiver = endpoint
                    endpoint = replace(caller, response_timeout=self.workload_response_timeout), receiver
                if self.record_svids:
                    from support.native_svid_observation import observe_svids

                    credentials[index] = observe_svids(endpoint[1], hop)
                endpoints[index] = fixture, endpoint
            invoke(start)
            if start:
                if chain.native_directory is None and operations[0] != "teleport-acquire":
                    assert lab.issuer.used, "Acquired X.509-SVID was not installed for the following workload hop"
                else:
                    observed = {sha256(certificate).hexdigest() for certificate in presented}
                    assert observed == {acquisition["acquired_sha256"]}, observed
                    trace[1]["presented_peer_sha256"] = observed.pop()
            decision = trace[-1]
            ledgers = {index: len(endpoint[1].ledger.snapshot()) for index, (_, endpoint) in endpoints.items()}
            assert all(not count for index, count in ledgers.items() if index != write_index), ledgers
            return {"reached_hops": len(trace), "decision_hop": decision["hop"],
                    "result": decision["result"], "effects": sum(ledgers.values()) + services.effects,
                    "trace": trace}
