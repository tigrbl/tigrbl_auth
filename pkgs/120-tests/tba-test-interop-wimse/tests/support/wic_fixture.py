from contextlib import contextmanager
from pathlib import Path
from threading import Thread

from cryptography.hazmat.primitives import serialization
from tba_testkit_workload_credential_conformance.fixtures import _certificate

from tba_test_interop_wimse.observations import Observation
from tba_test_interop_wimse.wic import (
    RejectedServerIdentity, TlsFiles, WicCaller, WicReceiver, WorkloadVerifier, certificate_status,
)

IDENTITY = "wimse://example.org/workload"
SERVER = IDENTITY + "/server"
DNS = "service.example.org"


def write_leaf(directory, name, leaf, anchor):
    certificate, key = leaf
    cert_path = directory / (name + ".pem")
    key_path = directory / (name + ".key")
    cert_path.write_bytes(certificate.public_bytes(serialization.Encoding.PEM))
    key_path.write_bytes(key.private_bytes(serialization.Encoding.PEM,
                                          serialization.PrivateFormat.PKCS8,
                                          serialization.NoEncryption()))
    return TlsFiles(str(cert_path), str(key_path), str(anchor))


class WicFixture:
    def __init__(self, directory, case, *, receiver_verifier=None, server_verifier=None,
                 scheme="wimse", external_verifier=None, direction=None, issue_pair=None,
                 caller_name="workload", receiver_name="workload/server"):
        self.case = case
        self.identity = f"{scheme}://example.org/{caller_name}"
        self.server_identity = f"{scheme}://example.org/{receiver_name}"
        variant = case["variant"]
        subjects = {
            "missing-workload-uri": (),
            "multiple-workload-uris": (self.identity, self.identity + "/other"),
            "untrusted-domain": (self.identity.replace("example.org", "outside.example"),),
        }.get(variant, (self.identity,))
        verifier_type = WorkloadVerifier
        if scheme == "spiffe":
            from tba_test_interop_wimse.spiffe_wic import SpiffeWicVerifier

            verifier_type = SpiffeWicVerifier
        if issue_pair is None:
            ca = _certificate(())
            anchor = directory / "ca.pem"
            anchor.write_bytes(ca[0].public_bytes(serialization.Encoding.PEM))
            self.server_tls = write_leaf(directory, "server", _certificate(
                (self.server_identity,), issuer=ca, dns=DNS if scheme == "wimse" else None
            ), anchor)
            self.client_tls = write_leaf(directory, "client", _certificate(subjects, issuer=ca), anchor)
        else:
            self.client_tls, self.server_tls = issue_pair(directory, subjects, self.server_identity)
            anchor = Path(self.client_tls.trust_anchor)
        client_anchor = Path(self.server_tls.trust_anchor)
        if variant == "wrong-anchor":
            # Keep the TLS CA fixed while varying the workload trust configuration.
            client_anchor = directory / "wrong-ca.pem"
            client_anchor.write_bytes(_certificate(())[0].public_bytes(serialization.Encoding.PEM))
        self.receiver_verifier = verifier_type(
            self.identity, {"example.org": client_anchor}, certificate_status([self.client_tls.certificate])
        )
        expected = self.server_identity + ("/other" if variant == "wrong-server-identity" else "")
        self.server_verifier = verifier_type(
            expected,
            {"example.org": anchor}, certificate_status([self.server_tls.certificate]),
        )
        if receiver_verifier:
            self.receiver_verifier = receiver_verifier(anchor, self.identity)
        if server_verifier:
            self.server_verifier = server_verifier(anchor, expected)
        if external_verifier and direction == "forward":
            self.receiver_verifier = external_verifier(
                client_anchor, self.identity, self.receiver_verifier.status,
            )
        if external_verifier and direction == "reverse":
            self.server_verifier = external_verifier(
                anchor, expected, self.server_verifier.status,
            )
    @contextmanager
    def running(self, *, authorize_write=None, authorize_read=None):
        with WicReceiver(
            0, self.server_tls, self.receiver_verifier, authorize_write=authorize_write,
            authorize_read=authorize_read,
        ) as receiver:
            thread = Thread(target=receiver.serve_forever, kwargs={"poll_interval": .01}, daemon=True)
            thread.start()
            try:
                yield WicCaller(self.client_tls, self.server_verifier), receiver
            finally:
                receiver.shutdown()
                thread.join(timeout=5)

    def observe(self, *, authorize_write=None, headers=None, check_response=None):
        with self.running(authorize_write=authorize_write) as (caller, receiver):
            try:
                result = caller.request("127.0.0.1", receiver.server_port, DNS, headers=headers)
            except RejectedServerIdentity as error:
                return Observation("deny", self.case["target_hop"],
                                   effects=len(receiver.ledger.snapshot()), reason=str(error))
            body = result["response"]
            if check_response is not None:
                check_response(result)
            if result["http_status"] == 201 or authorize_write is not None:
                readback = caller.request("127.0.0.1", receiver.server_port, DNS, readback=True)
                assert readback["http_status"] == 200
                assert readback["response"]["writes"] == list(receiver.ledger.snapshot())
            if result["http_status"] == 201:
                assert receiver.ledger.snapshot() == (self.identity,)
                assert body["decision"] == "allow" and body["identity"] == self.identity
            else:
                assert result["http_status"] == 403 and body["decision"] == "deny"
            return Observation(body["decision"], self.case["target_hop"],
                               effects=len(receiver.ledger.snapshot()),
                               reason=body.get("reason", body.get("identity", "")))


class NativeWicAdapter:
    def __init__(self, tmp_path):
        self.tmp_path = tmp_path

    def supports(self, case):
        return case["scenario_id"] in {"01", "02", "03"} and all(hop["profile"] == "wic-mtls" and hop["identifier_scheme"] in {"wimse", "spiffe"}
                   and hop["wic_issuer"] == "baseline" for hop in case["hops"].values())

    def setup_key(self, case, execution):
        return case["hops"][case["target_hop"]]["identifier_scheme"]

    def check_setup(self, case, execution):
        control = dict(case, variant="valid-peer", checker="receiver")
        with self.isolated(control, execution) as fixture:
            observed = fixture.observe()
            assert observed.decision == "allow" and observed.effects == 1

    @contextmanager
    def isolated(self, case, execution):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory(dir=self.tmp_path) as directory:
            yield WicFixture(Path(directory), case, scheme=self.setup_key(case, execution))
