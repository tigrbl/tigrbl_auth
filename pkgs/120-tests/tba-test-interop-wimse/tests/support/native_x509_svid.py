"""Mint short-lived native X.509-SVID credentials for the loopback lab."""

from cryptography.hazmat.primitives import serialization
from tba_concrete_x509_svid_credential import X509SvidCredential
from tba_test_interop_wimse.wic import TlsFiles
from tba_testkit_workload_credential_conformance.fixtures import _certificate

from support.wic_fixture import write_leaf


class NativeX509SvidIssuer:
    def __init__(self):
        self.authority = _certificate(())

    def mint(self, identity):
        leaf = _certificate((identity,), issuer=self.authority)
        chain = (leaf[0].public_bytes(serialization.Encoding.DER),
                 self.authority[0].public_bytes(serialization.Encoding.DER))
        X509SvidCredential(identity, chain)
        return leaf

    def issue_pair(self, directory, subjects, receiver):
        anchor = directory / "tba-svid-bundle.pem"
        root = self.authority[0].public_bytes(serialization.Encoding.PEM)
        anchor.write_bytes(root)
        server = write_leaf(directory, "server-svid", self.mint(receiver), anchor)
        if len(subjects) == 1 and subjects[0].startswith("spiffe://example.org/"):
            client = write_leaf(directory, "client-svid", self.mint(subjects[0]), anchor)
            return client, server
        # Inject negative inputs outside the registered issuer. TLS admits the
        # additional test CA so the workload verifier can inspect the leaf.
        foreign = _certificate(())
        transport_bundle = directory / "tls-input-roots.pem"
        transport_bundle.write_bytes(root + foreign[0].public_bytes(serialization.Encoding.PEM))
        client = write_leaf(directory, "foreign-input", _certificate(subjects, issuer=foreign), anchor)
        return client, TlsFiles(server.certificate, server.private_key, str(transport_bundle))
