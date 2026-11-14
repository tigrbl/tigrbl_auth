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
    def __init__(self, directory, case, *, receiver_verifier=None, server_verifier=None):
        self.case = case
        variant = case["variant"]
        subjects = {
            "missing-workload-uri": (),
            "multiple-workload-uris": (IDENTITY, IDENTITY + "/other"),
        }.get(variant, (IDENTITY,))
        ca = _certificate(())
        anchor = directory / "ca.pem"
        anchor.write_bytes(ca[0].public_bytes(serialization.Encoding.PEM))
        self.server_tls = write_leaf(directory, "server", _certificate((SERVER,), issuer=ca, dns=DNS), anchor)
        self.client_tls = write_leaf(directory, "client", _certificate(subjects, issuer=ca), anchor)
        self.receiver_verifier = WorkloadVerifier(
            IDENTITY, {"example.org": anchor}, certificate_status([self.client_tls.certificate])
        )
        self.server_verifier = WorkloadVerifier(
            SERVER if variant != "wrong-server-identity" else SERVER + "/other",
            {"example.org": anchor}, certificate_status([self.server_tls.certificate]),
        )
        if receiver_verifier:
            self.receiver_verifier = receiver_verifier(anchor, IDENTITY)
        if server_verifier:
            expected = SERVER if variant != "wrong-server-identity" else SERVER + "/other"
            self.server_verifier = server_verifier(anchor, expected)


    def observe(self):
        with WicReceiver(0, self.server_tls, self.receiver_verifier) as receiver:
            thread = Thread(target=receiver.serve_forever, kwargs={"poll_interval": .01}, daemon=True)
            thread.start()
            try:
                caller = WicCaller(self.client_tls, self.server_verifier)
                try:
                    result = caller.request("127.0.0.1", receiver.server_port, DNS)
                except RejectedServerIdentity as error:
                    return Observation("deny", self.case["target_hop"],
                                       effects=len(receiver.ledger.snapshot()), reason=str(error))
                body = result["response"]
                if result["http_status"] == 201:
                    readback = caller.request("127.0.0.1", receiver.server_port, DNS, readback=True)
                    assert readback["http_status"] == 200
                    assert readback["response"]["writes"] == [IDENTITY]
                    assert body["decision"] == "allow" and body["identity"] == IDENTITY
                else:
                    assert result["http_status"] == 403 and body["decision"] == "deny"
                return Observation(body["decision"], self.case["target_hop"],
                                   effects=len(receiver.ledger.snapshot()),
                                   reason=body.get("reason", body.get("identity", "")))
            finally:
                receiver.shutdown()
                thread.join(timeout=5)
