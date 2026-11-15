"""Resource adapters for combined mTLS and HTTP-signature cases."""

from contextlib import contextmanager
from types import SimpleNamespace
from urllib.parse import urlsplit

from tba_concrete_jwt import decode_jwt_unverified
from tba_provider_jose_cryptography.public_jws import public_jwk_key, verify_public_jws
from tba_test_interop_wimse.observations import Observation

from support.wic_fixture import DNS
from support.wic_services import TokenIssuer
from support.wic_support_cases import assert_ledger, request


def verify_spiffe_wit(serialized, *, trust_by_domain, now):
    token = decode_jwt_unverified(serialized)
    headers, claims = token.jws.protected_headers, token.claims
    subject = urlsplit(claims["sub"])
    keys = [key for key in trust_by_domain.get(subject.netloc, ()) if key.get("kid") == headers.get("kid")]
    if subject.scheme != "spiffe" or len(keys) != 1 or headers.get("typ") != "wit+jwt":
        raise ValueError("untrusted SPIFFE WIT-SVID")
    if not claims["iat"] <= now < claims["exp"]:
        raise ValueError("WIT-SVID outside validity period")
    verify_public_jws(serialized, keys[0])
    jwk = claims["cnf"]["jwk"]
    public_jwk_key(jwk, jwk["alg"])
    return token


class SignatureHop:
    def __init__(self, fixture, *, operation_variant="valid-peer"):
        self.fixture = fixture
        self.identity = fixture.identity
        self.server_identity = fixture.server_identity
        self.operation_variant = operation_variant
        self.context_token_header = ("X-Destination-Access-Token" if not fixture.signed else "Authorization")

    @contextmanager
    def running(self, **policies):
        application = self.fixture.caller("valid-peer")
        operation = (application if self.operation_variant == "valid-peer" else
                     self.fixture.caller(self.operation_variant))
        caller = self.fixture.combined_caller(application) if self.fixture.wic else application

        def proof_headers(port, *, readback=False, headers=None, dns=DNS, signed_path=None, signed_authority=None):
            options = {"signed_path": signed_path, "signed_authority": signed_authority} if self.fixture.signed else {}
            signer = application if readback else operation
            return signer.present(dns, port, readback=readback, extra_headers=headers, **options)

        def send(host, port, dns, *, readback=False, headers=None):
            proof = proof_headers(port, readback=readback, headers=headers, dns=dns)
            return caller.request(host, port, dns, readback=readback, headers=proof)

        with self.fixture.running(**policies) as server:
            yield SimpleNamespace(request=send, connection=caller.connection, proof_headers=proof_headers,
                                  send_proof=caller.request), server

    def observe(self, *, authorize_write=None, headers=None, check_response=None):
        with self.running(authorize_write=authorize_write) as endpoint:
            caller, server = endpoint
            result = caller.request("127.0.0.1", server.server_port, DNS, headers=headers)
            if check_response is not None:
                check_response(result)
            body = result["response"]
            return Observation(body["decision"], "enforcing", effects=len(assert_ledger(endpoint)),
                               reason=body.get("reason", body.get("identity", "")))


class SignatureBoundaryCase:
    def __init__(self, case, enforcing, *, gateway=None, transaction_issuer=None):
        self.case, self.enforcing, self.gateway = case, enforcing, gateway
        self.transaction_issuer = transaction_issuer

    def observe(self):
        variant = self.case["variant"]
        if self.gateway:
            return self.gateway.gateway(trusted_mapping=True)
        if self.case["scenario_id"] == "07":
            return self.transaction(variant)
        return self.proxy(variant)

    def transaction(self, variant):
        issuer = self.transaction_issuer or TokenIssuer("local-transaction", self.enforcing.server_identity)

        def enforce(identity, headers):
            claims = issuer.verify(headers.get("Txn-Token"))
            if (claims["sub"], claims["scope"]) != (identity, "write"):
                raise ValueError("transaction refused")

        with self.enforcing.running(authorize_write=enforce) as endpoint:
            caller, server = endpoint
            token = issuer.issue(self.enforcing.identity, "write")
            issuer.verify(token)
            headers = caller.proof_headers(server.server_port, headers={"txn-token": token})
            if variant == "token-binding-mismatch":
                headers["txn-token"] = issuer.issue(self.enforcing.identity, "write", nonce="substitute")
                assert headers["txn-token"] != token
                issuer.verify(headers["txn-token"])
            result = caller.send_proof("127.0.0.1", server.server_port, DNS, headers=headers)
            if variant == "token-binding-mismatch":
                reason = result["response"]["reason"].lower()
                assert "signature" in reason or "transaction token binding" in reason or "txn-token" in reason, result
            return self.result(result, endpoint)

    def proxy(self, variant):
        handoff = TokenIssuer("proxy-verifier", self.enforcing.server_identity)
        observed_by_proxy = []

        def authorize(identity, headers):
            if variant == "trusted-proxy-verification":
                claims = handoff.verify(headers.get("X-Proxy-Verification"))
                if claims["sub"] != identity or claims["scope"] != "write":
                    raise ValueError("proxy handoff refused")

        with self.enforcing.running(authorize_write=authorize) as endpoint:
            caller, server = endpoint
            if variant == "trusted-proxy-verification":
                def verify_before_forwarding(subject, _headers):
                    observed_by_proxy.append(subject)
                    raise ValueError("proxy-verified-write")

                # Authenticate a POST at the proxy and leave the effect to the
                # downstream service after it verifies the proxy handoff.
                with self.enforcing.running(authorize_write=verify_before_forwarding) as proxy:
                    response = request(proxy)
                    assert response["response"].get("reason") == "proxy-verified-write"
                    assert not proxy[1].ledger.snapshot()
                subject, = observed_by_proxy
                proof = caller.proof_headers(server.server_port, headers={
                    "X-Proxy-Verification": handoff.issue(subject, "write"),
                })
            else:
                proof = caller.proof_headers(
                    server.server_port,
                    signed_authority=(f"original.example.org:{server.server_port}"
                                      if variant == "signed-authority-changed" else None),
                    signed_path="/effects" if variant == "signed-path-changed" else None,
                )
            result = caller.send_proof("127.0.0.1", server.server_port, DNS, headers=proof)
            return self.result(result, endpoint)

    def result(self, response, endpoint):
        body = response["response"]
        assert response["http_status"] in {201, 401}, response
        return Observation(body["decision"], self.case["target_hop"], effects=len(assert_ledger(endpoint)),
                           reason=body.get("reason", body.get("identity", "")))
