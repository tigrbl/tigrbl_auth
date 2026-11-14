"""Direct and two-hop WIC cases with independently observed resource state."""

from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

from tba_test_interop_wimse.http_fixture import call_resource
from tba_test_interop_wimse.observations import Observation
from tba_test_interop_wimse.wic import RejectedServerIdentity

from support.wic_fixture import DNS
from support.wic_services import AccountingAuthority, BearerProvider, StatusAuthority, TokenIssuer

SUPPORT_FAMILIES = {
    "04": (),
    "08": ("source-token-issuer", "destination-access-token-issuer"),
    "12": ("status-authority", "effect-store"),
    "14": ("accounting-authority", "second-resource-service"),
    "17": ("approval-verifier",),
    "18": ("bearer-broker", "provider"),
    "20": ("source-token-issuer", "destination-access-token-issuer"),
}


def request(endpoint, *, read=False, **headers):
    caller, server = endpoint
    return caller.request("127.0.0.1", server.server_port, DNS, readback=read,
                          headers={name.replace("_", "-"): value for name, value in headers.items()})


def assert_ledger(endpoint):
    result = request(endpoint, read=True)
    writes = endpoint[1].ledger.snapshot()
    assert result["http_status"] == 200 and result["response"]["writes"] == list(writes), result
    return writes


def session_request(caller, connection, port, *, read=False, **headers):
    if hasattr(caller, "proof_headers"):
        headers = caller.proof_headers(port, readback=read, headers=headers)
    return call_resource(connection, readback=read, headers=headers, close=False)


class WicSupportFixture:
    def __init__(self, case, hops):
        self.case = case
        self.hops = hops
        self.ingress = hops.get("ingress")
        self.enforcing = hops["enforcing"]
        self.variant = case["variant"]

    def observe(self):
        run = {
            "04": self.gateway,
            "08": self.boundary,
            "12": self.before_effect,
            "14": self.budget,
            "17": self.approval,
            "18": self.bearer,
            "20": self.boundary,
        }
        return run[self.case["scenario_id"]]()

    def observation(self, result, server, **kwargs):
        body = result["response"]
        assert result["http_status"] in {201, 401, 403}, result
        return Observation(body["decision"], "enforcing", effects=len(server.ledger.snapshot()),
                           reason=body.get("reason", body.get("identity", "")), **kwargs)

    def gateway(self, *, trusted_mapping=False):
        origin = TokenIssuer("test-origin-proof", self.enforcing.server_identity)
        handoff = TokenIssuer("test-gateway-handoff", self.enforcing.server_identity)
        proof_header = "X-Origin-Proof"
        handoff_header = "X-Origin-Handoff"
        origin_identity = self.ingress.identity

        def enforce(identity, headers):
            assert identity == self.enforcing.identity
            if headers.get(proof_header):
                claims = origin.verify(headers[proof_header])
            elif headers.get(handoff_header):
                claims = handoff.verify(headers[handoff_header])
            else:
                raise ValueError("origin-identity-required")
            if (claims["sub"], claims["scope"]) != (origin_identity, "write"):
                raise ValueError("origin-authority-refused")

        forwarded = []
        with self.enforcing.running(authorize_write=enforce) as outbound:
            def forward(identity, headers):
                assert identity == origin_identity
                outgoing = {}
                if headers.get(proof_header):
                    outgoing["X_Origin_Proof"] = headers[proof_header]
                if self.variant == "trusted-origin-handoff" or trusted_mapping:
                    outgoing["X_Origin_Handoff"] = handoff.issue(identity, "write")
                forwarded.append(request(outbound, **outgoing))
                return {}

            with self.ingress.running(authorize_read=forward) as inbound:
                incoming = {}
                if self.variant == "validated-origin-proof":
                    incoming["X_Origin_Proof"] = origin.issue(origin_identity, "write")
                assert request(inbound, read=True, **incoming)["http_status"] == 200
            result, = forwarded
            writes = assert_ledger(outbound)
            assert not writes or writes == (self.enforcing.identity,)
            observation = self.observation(result, outbound[1])
            if self.variant == "missing-origin-identity":
                assert observation.reason == "origin-identity-required"
            return observation

    def boundary(self):
        source = TokenIssuer("source-test-domain", "source-resource")
        destination = TokenIssuer("destination-test-domain", self.enforcing.server_identity)
        events = []
        admitted = []
        context_header = getattr(self.enforcing, "context_token_header", "Authorization")

        def exchange(identity, headers):
            claims = source.verify(headers.get("Txn-Token"))
            if claims["sub"] != identity or claims["scope"] != "exchange":
                raise ValueError("source-transaction-refused")
            scope = "read" if self.variant == "authority-refused" else "write"
            token = destination.issue(self.enforcing.identity, scope)
            events.append("destination-access-token-issued")
            admitted.append(token)
            return {}

        def enforce(identity, headers):
            assert "Txn-Token" not in headers
            claims = destination.verify(headers.get(context_header))
            if (claims["sub"], claims["scope"]) != (identity, "write"):
                raise ValueError("destination-authority-refused")

        local_token = source.issue(self.ingress.identity, "exchange")
        events.append("local-token-issued")
        with self.ingress.running(authorize_read=exchange) as endpoint:
            assert request(endpoint, read=True, Txn_Token=local_token)["http_status"] == 200
            assert not endpoint[1].ledger.snapshot()
        token, = admitted
        if self.variant == "foreign-transaction-token":
            token = local_token
        with self.enforcing.running(authorize_write=enforce) as endpoint:
            try:
                result = request(endpoint, **{context_header: token})
            except RejectedServerIdentity as error:
                assert self.variant == "trust-refused" and "identity" in str(error)
                assert not endpoint[1].ledger.snapshot()
                return Observation("deny", "enforcing", reason=str(error))
            assert_ledger(endpoint)
            if result["http_status"] == 201:
                events.append("operation-allowed")
            if self.variant == "trust-refused":
                assert result["http_status"] in {401, 403}
                assert result["response"]["reason"] not in {
                    "issuer-signature-refused", "issuer-audience-refused", "destination-authority-refused",
                }
            if self.variant == "authority-refused":
                assert result["response"].get("reason") == "destination-authority-refused"
            if self.variant == "foreign-transaction-token":
                assert result["response"].get("reason") == "issuer-signature-refused"
            return self.observation(result, endpoint[1], events=tuple(events) if self.case["events"] else ())

    def before_effect(self):
        status = StatusAuthority()
        delegation = TokenIssuer("status-test-delegator", self.enforcing.server_identity)
        events = []
        measurements = {}

        def authorize_ingress(identity, headers):
            assert identity == self.ingress.identity
            return {"delegation": delegation.issue(self.enforcing.identity, "write")}

        def authorize(identity, headers):
            claims = delegation.verify(headers.get("X-Delegation"))
            if (claims["sub"], claims["scope"]) != (identity, "write"):
                raise ValueError("delegation-refused")
            if not status.permitted():
                events.append("revocation-observed")
                raise ValueError("revoked-before-effect")

        def preflight(identity, headers):
            if headers.get("X-Delegation"):
                authorize(identity, headers)
                events.append("initial-allow")
            return {}

        with self.ingress.running(authorize_read=authorize_ingress) as endpoint:
            initial = request(endpoint, read=True)
            assert initial["http_status"] == 200 and not endpoint[1].ledger.snapshot()
        headers = {"X-Delegation": initial["response"]["delegation"]}
        with self.enforcing.running(authorize_write=authorize, authorize_read=preflight) as endpoint:
            caller, server = endpoint
            connection = caller.connection("127.0.0.1", server.server_port, DNS)
            try:
                assert session_request(caller, connection, server.server_port, read=True, **headers)["http_status"] == 200
                tls_session = connection.sock
                assert tls_session is not None
                if self.variant == "revocation-before-effect":
                    status.publish_revocation()
                result = session_request(caller, connection, server.server_port, **headers)
                assert connection.sock is tls_session
            finally:
                connection.close()
            if result["http_status"] == 201:
                events.append("commit")
            else:
                assert result["response"].get("reason") == "revoked-before-effect"
                events.append("commit-refused")
                measurements = status.refusal()
            assert_ledger(endpoint)
            return self.observation(result, server, events=tuple(events), measurements=measurements)

    def budget(self):
        first = AccountingAuthority(limit=1)
        second = AccountingAuthority(limit=1) if self.case["accounting"] == "independent" else first
        audience = "shared-test-budget" if self.case["accounting"] else "ambiguous"
        with (self.ingress.running(authorize_write=first.authorize) as inbound,
              self.enforcing.running(authorize_write=second.authorize) as outbound):
            if self.case["schedule"] == "concurrent":
                start = Barrier(2, timeout=5)

                def send(endpoint):
                    start.wait()
                    return request(endpoint, X_Budget_Audience=audience)

                with ThreadPoolExecutor(max_workers=2) as pool:
                    responses = list(pool.map(send, (inbound, outbound)))
            else:
                responses = [request(endpoint, X_Budget_Audience=audience)
                             for endpoint in (inbound, outbound)]
            assert all(r["http_status"] in {201, 401, 403} for r in responses), responses
            reasons = [r["response"]["reason"] for r in responses if r["http_status"] in {401, 403}]
            writes = assert_ledger(inbound) + assert_ledger(outbound)
            debits = first.debits if first is second else first.debits + second.debits
            assert sorted(writes) == sorted(debits)
            if audience == "ambiguous":
                assert reasons == ["ambiguous-accounting-audience"] * 2
                return Observation("deny", "enforcing", effects=len(writes), reason=reasons[0])
            assert len(writes) == (1 if first is second else 2)
            assert reasons == (["budget-exhausted"] if first is second else [])
            return Observation("measure", "enforcing", effects=len(writes), budget_limit=first.limit,
                               measurements={"committed_debits": len(debits)})

    def approval(self):
        from support.oasnt_fixture import approval_token, verify_approval

        def authorize(identity, headers):
            assert identity == self.enforcing.identity
            verify_approval(headers.get("X-Approval"))

        observed = self.enforcing.observe(
            authorize_write=authorize, headers={"X-Approval": approval_token(self.variant)},
        )
        if self.variant == "oasnt-r2-display-mismatch":
            assert observed.reason == "display-mismatch"
        return observed

    def bearer(self):
        status = StatusAuthority()
        provider = BearerProvider()
        grant = TokenIssuer("test-broker-grant", self.enforcing.server_identity)
        phase = "initial"
        events = []
        scope = "read" if self.variant == "readonly-grant-write" else "write"
        token = grant.issue(self.enforcing.identity, scope)
        if self.variant == "missing-delegation":
            token = ""

        def broker(identity, headers):
            if not headers:
                return {}
            value = headers.get("X-Broker-Grant")
            if value is None:
                return {}
            try:
                claims = grant.verify(value)
                if (claims["sub"], claims["scope"]) != (identity, "write"):
                    raise ValueError("broker-scope-refused")
            except ValueError:
                events.append("broker-refused")
                raise
            if not status.permitted():
                events.extend(("revocation-observed", "release-refused"))
                raise ValueError("revoked-before-release")
            if phase == "initial":
                events.append("initial-allow")
                return {}
            bearer = provider.issue()
            events.append("bearer-released")
            return {"bearer": bearer}

        with self.enforcing.running(authorize_read=broker) as endpoint:
            result = request(endpoint, read=True, X_Broker_Grant=token)
            measurements = {}
            allowed = False
            if result["http_status"] in {401, 403}:
                assert not provider.tokens and "bearer" not in result["response"]
                events.append("no-bearer-release")
            else:
                assert result["http_status"] == 200
                phase = "release"
                if self.variant == "revocation-before-release":
                    status.publish_revocation()
                result = request(endpoint, read=True, X_Broker_Grant=token)
                if result["http_status"] == 200:
                    credential = result["response"]["bearer"]
                    if self.variant == "revocation-after-release":
                        status.publish_revocation()
                        assert not status.permitted()
                        events.append("revocation-observed")
                        allowed = provider.write(credential)
                        events.append("provider-decision")
                        # Check both sides of the expiry boundary with a deterministic clock.
                        provider.time = provider.ttl - 1
                        assert provider.time < provider.tokens[credential]
                        provider.time += 1
                        assert not provider.write(credential)
                        measurements = {"provider_allowed_after_revocation": int(allowed),
                                        "provider_expiry_seconds": provider.ttl}
                    else:
                        allowed = provider.write(credential)
                        assert allowed
                        events.append("provider-effect")
                else:
                    assert result["response"]["reason"] == "revoked-before-release"
                    assert not provider.tokens and "bearer" not in result["response"]
            assert not assert_ledger(endpoint)
            decision = "provider-policy" if "provider-decision" in events else "allow" if allowed else "deny"
            return Observation(decision, "enforcing", events=tuple(events), releases=len(provider.tokens),
                               effects=len(provider.effects), measurements=measurements,
                               reason=result["response"].get("reason", ""))
