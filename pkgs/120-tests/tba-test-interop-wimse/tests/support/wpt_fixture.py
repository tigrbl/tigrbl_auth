from contextlib import contextmanager
from tempfile import TemporaryDirectory
from pathlib import Path
from threading import Thread
from time import time
import json

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, utils
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from tba_concrete_jwt import decode_jwt_unverified
from tba_primitives_identity import base64url_encode
from tba_profile_workload_credential_wimse_wit import issue_wit
from tba_provider_jose_cryptography import JwsCryptographyProvider
from tba_provider_jose_cryptography.jws import sign_compact_jwt
from tba_testkit_workload_credential_conformance.fixtures import _certificate

from tba_test_interop_wimse.catalog import read_catalog
from tba_test_interop_wimse.composition import CombinedCaller
from tba_test_interop_wimse.httpsig import SignatureCaller, SignatureReceiver
from tba_test_interop_wimse.observations import Observation
from tba_test_interop_wimse.signatures import sign_request
from tba_test_interop_wimse.wic import RejectedServerIdentity
from tba_test_interop_wimse.wpt import WptCaller, WptReceiver

from support.wic_fixture import DNS, IDENTITY, write_leaf

def public_jwk(key):
    if isinstance(key, ec.EllipticCurvePrivateKey):
        coordinates = key.public_key().public_numbers()
        return {"kty": "EC", "crv": "P-256", "alg": "ES256",
                "x": base64url_encode(coordinates.x.to_bytes(32, "big")),
                "y": base64url_encode(coordinates.y.to_bytes(32, "big"))}
    return {"kty": "OKP", "crv": "Ed25519", "alg": "EdDSA",
            "x": base64url_encode(key.public_key().public_bytes_raw())}


def sign_wpt_claims(key, claims, algorithm):
    protected = {"typ": "wpt+jwt", "alg": algorithm}
    if algorithm == "EdDSA":
        return sign_compact_jwt(JwsCryptographyProvider({"proof": key}), claims,
                                headers=protected, key_reference="proof")
    if algorithm != "ES256":
        raise ValueError("unsupported fixture WPT algorithm")
    return sign_es256_jwt(key, claims, protected)


def sign_es256_jwt(key, claims, protected):
    if not isinstance(key, ec.EllipticCurvePrivateKey) or not isinstance(key.curve, ec.SECP256R1):
        raise ValueError("expected a P-256 signing key")
    header, payload = (base64url_encode(json.dumps(value, separators=(",", ":")).encode("ascii"))
                       for value in (protected, claims))
    message = f"{header}.{payload}"
    r, s = utils.decode_dss_signature(key.sign(message.encode("ascii"), ec.ECDSA(hashes.SHA256())))
    raw = r.to_bytes(32, "big") + s.to_bytes(32, "big")
    return f"{message}.{base64url_encode(raw)}"


class NativeWptAdapter:
    bindings = tuple(binding for binding in read_catalog("fixtures.toml")["local"].values()
                     if binding["profile"] != "wic-mtls")

    def __init__(self, directory):
        self.directory = directory

    def supports(self, case):
        hop = case["hops"][case["target_hop"]]
        return len(case["hops"]) == 1 and any(
            case["scenario_id"] in binding["families"]
            and (hop["profile"], hop["identifier_scheme"]) ==
                (binding["profile"], binding["identifier_scheme"])
            and hop["wit_issuer"] == "baseline" and hop["wic_issuer"] in ("baseline", "none")
            and (binding["profile"].startswith("wit-") or case["layer"] != "tls")
            and ("variants" not in binding or case["variant"] in binding["variants"])
            for binding in self.bindings
        )

    def setup_key(self, case, execution):
        hop = case["hops"][case["target_hop"]]
        return hop["profile"], hop["identifier_scheme"]

    def check_setup(self, case, execution):
        with self.isolated(dict(case, variant="valid-peer"), execution) as fixture:
            observation = fixture.observe()
            assert observation.decision == "allow" and observation.effects == 1

    @contextmanager
    def isolated(self, case, execution):
        with TemporaryDirectory(dir=self.directory) as work:
            yield WptFixture(Path(work), case)


class WptFixture:
    def __init__(self, directory, case, *, wic=None, signature_caller=None, signature_receiver=None,
                 identity=IDENTITY, issued_wit=None, proof_caller=None, proof_receiver=None):
        self.case = case
        hop = case.get("hops", {}).get(case.get("target_hop"), {})
        self.profile = hop.get("profile", "wit-wpt")
        self.signed = self.profile.endswith("http-signature")
        self.signature_caller = signature_caller or SignatureCaller
        self.signature_receiver = signature_receiver or SignatureReceiver
        self.proof_caller = proof_caller
        self.proof_receiver = proof_receiver or WptReceiver
        self.identity = identity
        self.server_identity = wic.server_identity if wic else DNS
        self.issued_wit = issued_wit
        issuer, workload, alternate = (Ed25519PrivateKey.generate() for _ in range(3))
        self.signer = JwsCryptographyProvider(
            {"issuer": issuer, "workload": workload, "alternate": alternate}
        )
        self.workload = public_jwk(workload)
        self.workload_key = workload
        self.trust = {"example.org": [{**public_jwk(issuer), "kid": "fixture-issuer"}]}
        if issued_wit is not None:
            _, self.workload_key, public = issued_wit(identity)
            self.trust = {"example.org": [public]}
        self.wic = None
        if self.profile.startswith("wic-"):
            from support.wic_fixture import WicFixture

            self.wic = wic or WicFixture(directory, case, scheme=hop["identifier_scheme"])
            self.tls = self.wic.server_tls
            self.anchor = Path(self.tls.trust_anchor)
            return
        ca = _certificate(())
        self.anchor = directory / "ca.pem"
        self.anchor.write_bytes(ca[0].public_bytes(serialization.Encoding.PEM))
        self.tls = write_leaf(directory, "server", _certificate((), issuer=ca, dns=DNS), self.anchor)

    def caller(self, variant):
        now = int(time())
        subject = self.identity.replace("example.org", "other.example") if variant == "untrusted-domain" else self.identity
        if variant == "identity-equality-policy":
            subject += "/different"
        if self.issued_wit is not None:
            wit, key, _ = self.issued_wit(subject, alternate=variant == "wrong-anchor")
            endpoint = self.signature_caller if self.signed else self.proof_caller
            return endpoint(key, wit, "workload", str(self.anchor))
        wit = issue_wit(
            self.signer, subject=subject, confirmation_jwk=self.workload,
            issuer_key_reference="alternate" if variant == "wrong-anchor" else "issuer",
            issuer_key_id="fixture-issuer", issuer_algorithm="EdDSA",
            issued_at=now, expires_at=now + 120,
        )
        if self.signed:
            return self.signature_caller(self.workload_key, wit, "workload", str(self.anchor))
        if self.proof_caller:
            return self.proof_caller(self.workload_key, wit, "workload", str(self.anchor))
        return WptCaller(self.signer, wit, "workload", str(self.anchor))

    def request(self, caller, port, **options):
        if self.wic:
            caller = CombinedCaller(caller, self.wic.client_tls, self.wic.server_verifier)
        return caller.request("127.0.0.1", port, DNS, **options)

    def proof_headers(self, caller, port, *, readback=False, headers=None):
        if not self.signed:
            assert not headers
            return caller.present(DNS, port, readback=readback)
        return caller.present(DNS, port, readback=readback, extra_headers=headers)

    def combined_caller(self, caller):
        return CombinedCaller(caller, self.wic.client_tls, self.wic.server_verifier)

    @contextmanager
    def running(self, *, authorize_write=None, authorize_read=None):
        variant = self.case["variant"]
        endpoint = self.signature_receiver if self.signed else self.proof_receiver
        transport = ({
            "client_tls": self.tls, "client_verifier": self.wic.receiver_verifier,
            "identity_pairs": {(self.wic.identity, self.identity)}
            if variant != "identity-equality-policy" else (),
        } if self.wic else {})
        with endpoint(0, self.tls.certificate, self.tls.private_key, DNS, self.trust,
                      authorize_write=authorize_write, authorize_read=authorize_read,
                      **transport) as receiver:
            thread = Thread(target=receiver.serve_forever, kwargs={"poll_interval": .01}, daemon=True)
            thread.start()
            try:
                yield receiver
            finally:
                receiver.shutdown()
                thread.join(timeout=5)

    def observe(self):
        variant = self.case["variant"]
        with self.running() as receiver:
            caller = self.caller(variant)
            port = receiver.server_port
            headers = caller.present("other.example" if variant == "wrong-audience" else DNS, port)
            if variant == "missing-proof":
                headers.pop("signature" if self.signed else "Authorization")
            if variant == "wrong-proof-key":
                if self.signed:
                    if getattr(caller, "cofide", False):
                        from dataclasses import replace

                        wrong = replace(caller, signer=ec.generate_private_key(ec.SECP256R1()))
                        headers = wrong.present(DNS, port)
                    else:
                        headers = sign_request(Ed25519PrivateKey.generate(), caller.wit, "POST",
                                               "/writes", f"https://{DNS}:{port}/writes", int(time()))
                else:
                    claims = decode_jwt_unverified(headers["Authorization"].split(" ", 1)[1]).claims
                    algorithm = decode_jwt_unverified(caller.wit).claims["cnf"]["jwk"]["alg"]
                    wrong_key = (ec.generate_private_key(ec.SECP256R1()) if algorithm == "ES256"
                                 else Ed25519PrivateKey.generate())
                    proof = sign_wpt_claims(wrong_key, claims, algorithm)
                    headers["Authorization"] = "WPT " + proof
            try:
                result = self.request(caller, port, headers=headers)
            except RejectedServerIdentity as error:
                if self.case.get("layer") != "tls":
                    raise
                assert not receiver.ledger.snapshot()
                return Observation("deny", self.case["target_hop"], reason=str(error))
            events = ()
            additional = 0
            decision = result["response"]["decision"]
            if variant == "duplicate-presentation":
                assert result["http_status"] == 201
                assert receiver.ledger.snapshot() == (self.identity,)
                result = self.request(caller, port, headers=headers)
                assert result["http_status"] == 401
                assert result["response"]["decision"] == "deny"
                additional = len(receiver.ledger.snapshot()) - 1
                events = ("initial-allow", "initial-effect", "duplicate-refused")
                decision = "allow-then-deny"
            elif decision == "allow":
                assert result["http_status"] == 201
                assert result["response"]["identity"] == self.identity
            else:
                assert result["http_status"] == 401
            writes = receiver.ledger.snapshot()
            if self.case.get("layer") != "tls" and (
                variant != "identity-equality-policy" or not self.wic or self.wic.identity == self.identity
            ):
                readback = self.request(self.caller("valid-peer"), port, readback=True)
                assert readback["http_status"] == 200, (result, readback)
                assert readback["response"]["writes"] == list(writes)
            return Observation(decision, self.case["target_hop"], events,
                               effects=len(writes), additional_effects=additional,
                               reason=result["response"].get("reason", self.identity))

