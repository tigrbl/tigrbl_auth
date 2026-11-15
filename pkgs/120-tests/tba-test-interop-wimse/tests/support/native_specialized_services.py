"""Native transaction-token and delegation-receipt services for typed flows."""

from hashlib import sha256
from secrets import token_urlsafe

from support.native_acquired_policy import NativeAcquiredPolicyBindings
from support.typed_hop_adapters import observe_http
from support.wic_services import TokenIssuer


TRANSACTION = "tba-txn-issue"
RECEIPT = "tba-receipt-check"


def digest(value):
    return sha256(value.encode()).hexdigest()


class NativeSpecializedBindings(NativeAcquiredPolicyBindings):
    bindings = {
        **NativeAcquiredPolicyBindings.bindings,
        TRANSACTION: {"tba-transaction-token-issuer"},
        RECEIPT: {"tba-delegation-receipt-verifier"},
    }

    def __init__(self, hops, agent_factory=None):
        super().__init__(hops, agent_factory)
        self.transaction = None
        self.transaction_verified = {}
        self.receipt_issuer = TokenIssuer("tba-delegation-authority", "tba-delegation-receipt-verifier")
        self.receipts = []

    def headers(self, index, fault, fixture):
        headers = super().headers(index, fault, fixture)
        if index == 1 and self.transaction:
            headers["txn-token"] = self.transaction
        return headers

    def authorize(self, index, identity, headers, fault, fixture):
        super().authorize(index, identity, headers, fault, fixture)
        if index == 1 and self.transaction:
            token = headers.get("txn-token")
            claims = self.claims(self.source, token, self.hops[index]["caller"], {"write"})
            assert identity.rsplit("/", 1)[-1] == claims["sub"]
            assert token == self.transaction
            self.transaction_verified[index] = digest(token)

    def workload_evidence(self, index):
        if index in self.transaction_verified:
            return {"verified_transaction_sha256": self.transaction_verified[index]}
        return super().workload_evidence(index)

    def source_transaction(self, actor, fault):
        if self.transaction and not fault:
            return self.transaction
        return super().source_transaction(actor, fault)

    def support_request(self, index, fault):
        hop = self.hops[index]
        operation = hop["operation"]
        if operation == TRANSACTION:
            return self.transaction_request(hop, fault)
        if operation == RECEIPT:
            return self.verify_receipts(hop, fault)
        outcome = super().support_request(index, fault)
        if operation == "delegate" and outcome["decision"] == "allow":
            previous = digest(self.receipts[-1]["receipt"]) if self.receipts else ""
            receipt = self.receipt_issuer.issue(hop["receiver"], digest(self.grant), nonce=previous)
            self.receipts.append({"grant": self.grant, "receipt": receipt})
        if operation == "source-exchange" and self.transaction and outcome["decision"] == "allow":
            outcome["verified_transaction_sha256"] = digest(self.transaction)
        return outcome

    def transaction_request(self, hop, fault):
        authorization = self.resource.issue(hop["caller"], "read" if fault else "issue")

        def issue(request):
            try:
                self.claims(self.resource, request["authorization"], hop["caller"], {"issue"})
            except ValueError:
                return self.refusal("transaction-token-request-refused")
            return self.accepted("transaction-token-issued", token=self.source.issue(
                hop["caller"], "write exchange", nonce=token_urlsafe(18),
            ))

        result = self.support_observation({"authorization": authorization}, issue)
        if result["decision"] == "allow":
            self.transaction = result.pop("token")
            result["issued_transaction_sha256"] = digest(self.transaction)
        return {**result, "support_role": hop["support"]}

    def verify_receipts(self, hop, fault):
        records = [dict(record) for record in self.receipts]
        if fault:
            records[-1]["receipt"] += "x"

        def verify(request):
            received = request["receipts"]
            previous = ""
            try:
                assert len(received) == len(self.hops) - 1
                for record, delegation_hop in zip(received, self.hops):
                    child = delegation_hop["receiver"]
                    self.claims(self.delegation, record["grant"], child, {"write"})
                    signed = self.receipt_issuer.verify(record["receipt"])
                    assert (signed["sub"], signed["scope"], signed["nonce"]) == (
                        child, digest(record["grant"]), previous,
                    )
                    previous = digest(record["receipt"])
                assert child == hop["caller"]
            except (AssertionError, ValueError):
                return self.refusal("invalid-delegation-receipt-refused")
            return self.accepted("narrowed-receipt-accepted", verified_receipts=len(received))

        result = self.support_observation({"receipts": records}, verify)
        return {**result, "support_role": hop["support"]}

    @staticmethod
    def support_observation(payload, evaluate):
        result = observe_http(payload, evaluate)
        assert result.pop("reached_hops") == result.pop("decision_hop") == 1
        assert result.pop("effects") == 0
        return result
