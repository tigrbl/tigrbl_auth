"""Execute a typed workload chain using the independently qualified endpoints."""

from contextlib import contextmanager, ExitStack
from functools import lru_cache
from pathlib import Path
from tempfile import TemporaryDirectory

from tba_test_interop_wimse.qualification import pair_has_baseline
from tba_test_interop_wimse.native_expansion import COMBINED_SCOPE, matches_native_issuer_scope

from support.signature_cases import SignatureHop
from support.wic_fixture import WicFixture
from support.wic_support_cases import request
from support.wimsey_wpt import wpt_endpoints
from support.wpt_fixture import WptFixture


@contextmanager
def native_workload_hop(directory, case, hop, names, *, acquired=None, presented=None):
    with TemporaryDirectory(dir=directory) as work:
        location = Path(work)
        profile = hop["profile"]
        wic = None
        if profile.startswith("wic-"):
            transport = case if case["layer"] == "tls" else dict(case, variant="valid-peer")
            if profile == "wic-mtls":
                transport = case
            issue_pair = None
            if hop["wic_issuer"] == "tba-x509-svid":
                from support.native_x509_svid import NativeX509SvidIssuer

                issue_pair = (acquired or NativeX509SvidIssuer()).issue_pair
            wic = WicFixture(location, transport, scheme=hop["identifier_scheme"], issue_pair=issue_pair, **names)
            if presented is not None:
                verify = wic.receiver_verifier.verify

                def observe_certificate(certificate, **options):
                    presented(certificate)
                    return verify(certificate, **options)

                wic.receiver_verifier.verify = observe_certificate
        if profile == "wic-mtls":
            yield wic
            return
        use_wit_svid = hop["wit_issuer"] == "tba-wit-svid"
        options = {}
        if profile.endswith("wpt"):
            caller, receiver = wpt_endpoints(None, None, None, spire=use_wit_svid)
            options = {"proof_caller": caller, "proof_receiver": receiver}
        elif use_wit_svid:
            from support.native_wit_svid import NativeWitSvidSignatureReceiver

            options["signature_receiver"] = NativeWitSvidSignatureReceiver
        proof_case = dict(case, variant="valid-peer") if case["layer"] == "tls" else case
        scheme = "spiffe" if use_wit_svid else "wimse"
        issued_wit = None
        if use_wit_svid:
            from support.native_wit_svid import NativeWitSvidIssuer

            issued_wit = NativeWitSvidIssuer().mint
        yield WptFixture(
            location, proof_case, wic=wic, identity=f"{scheme}://example.org/{names['caller_name']}",
            issued_wit=issued_wit, **options,
        )


class TypedWorkloadChain:
    def __init__(self, peers, get_lab=None, *, native_directory=None, native_wit_svid=False,
                 native_x509_svid=False, native_combined_svid=False):
        self.peers = peers
        self.get_lab = get_lab
        self.native_directory = native_directory
        self.native_wit_svid = native_wit_svid
        self.native_x509_svid = native_x509_svid
        self.native_combined_svid = native_combined_svid

    @lru_cache(maxsize=None)
    def qualified(self, caller_pin, receiver_pin, profile, scheme, wic_issuer, wit_issuer):
        pair = {}
        for role, pin in (("caller", caller_pin), ("receiver", receiver_pin)):
            match = next((
                row for row in self.peers["capabilities"]
                if row["role"] == role and row["profile"] == profile
                and row["identifier_scheme"] == scheme and row["status"] == "qualified"
                and tuple(row.get(key) for key in ("implementation", "version", "configuration")) == pin
            ), None)
            if match is None:
                return False
            pair[role] = match
        if self.native_directory is not None:
            return (caller_pin[0] == receiver_pin[0] == "tba"
                    and (wic_issuer in ("none", "baseline")
                         or self.native_x509_svid and wic_issuer == "tba-x509-svid")
                    and (wit_issuer in ("none", "baseline")
                         or self.native_wit_svid and wit_issuer == "tba-wit-svid"))
        if not pair_has_baseline(self.peers, pair):
            return False
        for kind, issuer in (("wic_issuer", wic_issuer), ("wit_issuer", wit_issuer)):
            if issuer == "none":
                continue
            support = self.peers.get("qualified_support", {}).get(f"enforcing:{kind}:{issuer}", {})
            if not any(
                binding.get("profile") == profile and scheme in binding.get("identifier_schemes", ())
                and all(row["configuration"] == binding.get("endpoint_configuration", binding.get("configuration"))
                        for row in pair.values())
                for binding in support.get("bindings", [support])
            ):
                return False
        return True

    def supports(self, execution):
        if (self.native_directory is not None and not self.native_combined_svid
                and matches_native_issuer_scope(execution["hops"], COMBINED_SCOPE)):
            return False
        return all(self.qualified(
            tuple(hop["caller_pin"]), tuple(hop["receiver_pin"]), hop["profile"],
            hop["identifier_scheme"], hop["wic_issuer"], hop["wit_issuer"],
        ) for hop in execution["hops"])

    def observe(self, execution):
        hops = execution["hops"]
        fault = execution["outcome_id"]
        target, _, requested_fault = fault.partition(":")
        lab = self.get_lab() if self.get_lab else None
        trace = []
        endpoints = {}
        with ExitStack() as stack:
            def invoke(index):
                trace.append({"hop": index + 1})
                record = trace[-1]
                result = request(endpoints[index], read=index < len(hops) - 1)
                record.update(result["response"], http_status=result["http_status"])
                assert result["http_status"] in {200, 201, 401, 403}, result

            for index, hop in reversed(list(enumerate(hops))):
                number = str(index + 1)
                last = index == len(hops) - 1
                wrong_identity = number == target and requested_fault == "peer-identity-refused"
                scope = "read" if number == target and requested_fault == "operation-scope-refused" else "write"
                transport_fault = wrong_identity and hop["profile"] == "wic-mtls"
                case = {
                    "scenario_id": "01", "variant": "wrong-anchor" if transport_fault else "valid-peer",
                    "layer": "tls" if transport_fault else "operation",
                    "hops": {number: hop}, "target_hop": number,
                }
                direction = "forward" if hop["caller_pin"][0] == "tba" else "reverse"
                names = {"caller_name": hop["caller"], "receiver_name": hop["receiver"]}
                binding = (native_workload_hop(self.native_directory, case, hop, names)
                           if self.native_directory is not None else lab.signature.hop(case, direction, hop, names))
                fixture = stack.enter_context(binding)
                if isinstance(fixture, WptFixture):
                    variant = "wrong-anchor" if wrong_identity else "valid-peer"
                    fixture = SignatureHop(
                        fixture, operation_variant=variant if last else "valid-peer",
                        read_variant=variant if not last else "valid-peer",
                    )

                def authorize(identity, headers, *, expected=fixture.identity,
                              grant=scope, next_index=index + 1, final=last):
                    assert identity == expected
                    if grant != "write":
                        raise ValueError("operation-scope-refused")
                    if not final:
                        invoke(next_index)
                    return {}

                endpoints[index] = stack.enter_context(fixture.running(
                    authorize_write=authorize if last else None,
                    authorize_read=authorize if not last else None,
                ))
            invoke(0)
            decision = trace[-1]
            for record in trace[:-1]:
                assert (record["decision"], record["http_status"]) == ("allow", 200), trace
            if decision["decision"] == "allow":
                assert decision["http_status"] == 201, trace
                result = "operation-authorized"
            else:
                assert decision["decision"] == "deny" and decision["http_status"] in {401, 403}, trace
                result = ("operation-scope-refused" if decision.get("reason") == "operation-scope-refused"
                          else "peer-identity-refused")
            ledgers = [endpoints[index][1].ledger.snapshot() for index in range(len(hops))]
            assert not any(ledgers[:-1]), ledgers
            return {
                "reached_hops": len(trace), "decision_hop": decision["hop"], "result": result,
                "effects": sum(map(len, ledgers)), "trace": trace,
            }
