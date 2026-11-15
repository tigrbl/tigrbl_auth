"""Loopback authority, token-exchange, broker, and provider bindings."""

from copy import copy

from support.typed_hop_adapters import observe_http
from support.typed_service_flow import StatusFlowServices
from support.wic_services import BearerProvider, StatusAuthority, TokenIssuer


class TypedServiceBindings(StatusFlowServices):
    bindings = {
        **StatusFlowServices.bindings,
        "delegate": {"lab-delegation-authority"},
        "redeem-delegation": {"lab-delegation-token-server"},
        "source-exchange": {"source-token-issuer"},
        "destination-exchange": {"destination-access-token-issuer"},
        "provider": {"planned-bearer-provider-endpoint", "planned-tba-bearer-provider"},
        "acquire": {"planned-spire-agent-workload-api"},
    }

    def __init__(self, hops, agent_factory=None):
        super().__init__(hops, agent_factory)
        self.agent_factory = agent_factory
        self.acquired_issuer = None
        self.delegation = TokenIssuer("native-delegation", "typed-delegate")
        self.source = TokenIssuer("source-domain", "source-exchange")
        self.destination = TokenIssuer("destination-domain", "destination-exchange")
        self.resource = TokenIssuer("destination-resource", "typed-workload")
        self.broker = TokenIssuer("broker-authority", "typed-broker")
        self.provider = BearerProvider()
        self.grant = None
        self.call_context = None
        self.bearer = None
        self.broker_grant = None

    @staticmethod
    def refusal(reason):
        return {"decision": "deny", "result": reason}

    @staticmethod
    def accepted(result, **output):
        return {"decision": "allow", "result": result, **output}

    @staticmethod
    def claims(issuer, token, actor, required):
        claims = issuer.verify(token)
        if claims["sub"] != actor or not required <= set(claims["scope"].split()):
            raise ValueError("subject or scope does not match")
        return claims

    def headers(self, index, fault, fixture):
        operation = self.hops[index]["operation"]
        actor = self.hops[index]["caller"]
        header = getattr(fixture, "context_token_header", "X-Destination-Access-Token")
        if operation == "broker":
            grant = (self.broker.issue(actor, "read") if fault == "broker-grant-refused" else
                     self.broker_grant or self.broker.issue(actor, "write"))
            return {header: grant}
        if operation == "boundary-call":
            issuer = self.source if fault == "foreign-domain-token-refused" else self.resource
            return {header: issuer.issue(actor, "write")}
        if self.call_context:
            signer, actor_with_grant, token = self.call_context
            if actor == actor_with_grant:
                return {header: token}
        return {}

    def authorize(self, index, identity, headers, fault, fixture):
        super().authorize(index, identity, headers, fault, fixture)
        hop = self.hops[index]
        operation, actor = hop["operation"], hop["caller"]
        header = getattr(fixture, "context_token_header", "X-Destination-Access-Token")
        if operation == "boundary-call":
            try:
                self.claims(self.resource, headers.get(header), actor, {"write"})
            except ValueError as error:
                raise ValueError("foreign-domain-token-refused") from error
            self.broker_grant = self.broker.issue(hop["receiver"], "write")
        elif operation == "broker":
            try:
                self.claims(self.broker, headers.get(header), actor, {"write"})
            except ValueError as error:
                raise ValueError("broker-grant-refused") from error
            status = StatusAuthority()
            if fault == "revocation-before-provider-call":
                status.publish_revocation()
            if not status.permitted():
                raise ValueError("revocation-before-provider-call")
            self.bearer = self.provider.issue()
        elif self.call_context:
            signer, actor_with_grant, _ = self.call_context
            if actor != actor_with_grant:
                raise ValueError("resource grant has the wrong actor")
            self.claims(signer, headers.get(header), actor, {"write"})
            receiver = hop["receiver"]
            self.call_context = signer, receiver, signer.issue(receiver, "write")

    def configure_lab(self, lab):
        if self.acquired_issuer is None:
            return lab
        configured = copy(lab)
        configured.issuer = self.acquired_issuer
        return configured

    def source_transaction(self, actor, fault):
        issuer = self.destination if fault else self.source
        return issuer.issue(actor, "exchange")

    def support_request(self, index, fault):
        hop = self.hops[index]
        operation, actor = hop["operation"], hop["caller"]
        if operation == "check":
            return super().support_request(index, fault)
        if operation == "acquire":
            agent = self.agent_factory()
            material = agent.fetch(enrolled=not fault)
            if material is None:
                return self.refusal("workload-not-entitled-to-svid")
            self.acquired_issuer = agent.with_acquired(material)
            if hop["support"] == "planned-tba-workload-api":
                return self.accepted("x509-svid-delivered", grpc_status="OK", acquired_sha256=material.fingerprint)
            return self.accepted("x509-svid-delivered")
        if operation == "provider":
            token = "unrecognized-bearer" if fault else self.bearer

            def evaluate(_, headers):
                scheme, _, credential = headers.get("Authorization", "").partition(" ")
                if scheme != "Bearer" or not self.provider.write(credential):
                    return self.refusal("provider-credential-refused")
                return self.accepted("provider-committed-one-effect")

            result = observe_http({}, evaluate, headers={"Authorization": f"Bearer {token}"})
            self.effects = len(self.provider.effects)
        elif operation == "delegate":
            parent = self.grant or self.delegation.issue(actor, "read write")
            scope = "admin" if fault else "write"

            def evaluate(payload):
                try:
                    self.claims(self.delegation, payload["parent"], payload["actor"], {payload["scope"]})
                except ValueError:
                    return self.refusal("delegation-widens-parent-scope")
                token = self.delegation.issue(payload["delegate"], payload["scope"])
                return self.accepted("narrowed-authority-issued", grant=token)

            receiver = hop["receiver"]
            result = observe_http({"actor": actor, "delegate": receiver, "parent": parent, "scope": scope}, evaluate)
            if result["decision"] == "allow":
                self.grant = result["grant"]
                self.call_context = self.delegation, receiver, self.grant
        elif operation == "redeem-delegation":
            grant = self.delegation.issue("other-workload", "write") if fault else self.grant

            def evaluate(payload):
                try:
                    self.claims(self.delegation, payload["grant"], payload["actor"], {"write"})
                except ValueError:
                    return self.refusal("grant-not-bound-to-delegate")
                return self.accepted("delegate-access-token-issued", token=self.resource.issue(payload["actor"], "write"))

            result = observe_http({"actor": actor, "grant": grant}, evaluate)
            if result["decision"] == "allow":
                self.call_context = self.resource, actor, result["token"]
        elif operation == "source-exchange":
            transaction = self.source_transaction(actor, fault)

            def evaluate(payload):
                try:
                    self.claims(self.source, payload["transaction"], payload["actor"], {"exchange"})
                except ValueError:
                    return self.refusal("source-transaction-token-refused")
                return self.accepted("destination-authorization-grant-issued",
                                     grant=self.destination.issue(payload["actor"], "exchange"))

            result = observe_http({"actor": actor, "transaction": transaction}, evaluate)
            if result["decision"] == "allow":
                self.grant = result["grant"]
        elif operation == "destination-exchange":
            grant = (self.source.issue(actor, "exchange") if fault else
                     self.grant or self.destination.issue(actor, "exchange"))

            def evaluate(payload):
                try:
                    self.claims(self.destination, payload["grant"], payload["actor"], {"exchange"})
                except ValueError:
                    return self.refusal("authorization-grant-refused")
                return self.accepted("destination-access-token-issued",
                                     token=self.resource.issue(payload["actor"], "write"))

            result = observe_http({"actor": actor, "grant": grant}, evaluate)
            if result["decision"] == "allow":
                self.call_context = self.resource, actor, result["token"]
        else:
            raise ValueError(f"Unregistered support operation: {operation}")
        assert result["reached_hops"] == 1 and result["decision_hop"] == 1
        return {"decision": result["decision"], "result": result["result"]}


class NativeAcquisitionBindings(TypedServiceBindings):
    bindings = {**TypedServiceBindings.bindings, "acquire": {"planned-tba-workload-api"}}

    def support_request(self, index, fault):
        result = super().support_request(index, fault)
        if self.hops[index]["operation"] == "acquire" and result["decision"] == "deny":
            result["grpc_status"] = "PERMISSION_DENIED"
        return result
