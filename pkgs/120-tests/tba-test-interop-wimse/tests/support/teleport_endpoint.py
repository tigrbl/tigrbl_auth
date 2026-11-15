"""Fetch live Teleport X.509-SVIDs and bind them to the next mTLS call."""

from dataclasses import replace
from pathlib import Path
from uuid import uuid4

from cryptography import x509
from cryptography.hazmat.primitives import hashes

from tba_test_interop_wimse.wic import TlsFiles

from support.spire_issuer import docker
from support.spire_workload_api import AGENT, SOCKET, AcquiredIssuer
from support.typed_service_bindings import TypedServiceBindings


OPERATION = "teleport-acquire"
ISSUER = "teleport-x509-svid"


class TeleportWorkloadAPI:
    def __init__(self, container, directory, issuer=None):
        self.container = container
        self.directory = Path(directory)
        self.issuer = issuer

    def image(self):
        return docker("inspect", "--format", "{{.Image}}", self.container).stdout.strip()

    def fetch(self, *, enrolled):
        identifier = uuid4().hex
        remote = f"/tmp/tba-acquired/{identifier}"
        args = ("-u", "0" if enrolled else "1001", self.container, AGENT,
                "api", "fetch", "x509", "-socketPath", SOCKET, "-timeout", "5s")
        if not enrolled:
            reply = docker("exec", *args, check=False)
            detail = reply.stdout + reply.stderr
            if reply.returncode and "attributes did not pass rule evaluation" in detail:
                return None
            raise ValueError("Teleport did not report a Unix attestation refusal")
        docker("exec", self.container, "/busybox/mkdir", "-p", remote)
        directory = self.directory / identifier
        directory.mkdir()
        try:
            docker("exec", *args, "-write", remote)
            docker("cp", f"{self.container}:{remote}/.", directory)
        finally:
            docker("exec", self.container, "/busybox/rm", "-f",
                   *(f"{remote}/{name}" for name in ("svid.0.pem", "svid.0.key", "bundle.0.pem")))
            docker("exec", self.container, "/busybox/rmdir", remote)
        certificate = directory / "svid.0.pem"
        key = directory / "svid.0.key"
        bundle = directory / "bundle.0.pem"
        leaf, = x509.load_pem_x509_certificates(certificate.read_bytes())
        identity, = leaf.extensions.get_extension_for_class(x509.SubjectAlternativeName).value
        if identity.value != "spiffe://example.org/workload-0":
            raise ValueError("Teleport returned an unexpected SPIFFE identity")
        anchor, = x509.load_pem_x509_certificates(bundle.read_bytes())
        leaf.verify_directly_issued_by(anchor)
        return TlsFiles(str(certificate), str(key), str(bundle))

    def with_acquired(self, material):
        return TeleportAcquiredIssuer(self.issuer, material)


class TeleportAcquiredIssuer(AcquiredIssuer):
    def issue_pair(self, directory, subjects, receiver):
        client, server = super().issue_pair(directory, subjects, receiver)
        if self.used and client is self.material:
            return (replace(client, trust_anchor=server.trust_anchor),
                    replace(server, trust_anchor=client.trust_anchor))
        return client, server


def fingerprint(material):
    return x509.load_pem_x509_certificate(Path(material.certificate).read_bytes()).fingerprint(hashes.SHA256()).hex()


class TeleportBindings(TypedServiceBindings):
    bindings = {**TypedServiceBindings.bindings, OPERATION: {"teleport-tbot"}}

    def support_request(self, index, fault):
        if self.hops[index]["operation"] != OPERATION:
            return super().support_request(index, fault)
        agent = self.agent_factory()
        material = agent.fetch(enrolled=not fault)
        if material is None:
            return self.refusal("workload-not-entitled-to-svid")
        self.acquired_issuer = agent.with_acquired(material)
        return self.accepted("x509-svid-delivered", acquired_sha256=fingerprint(material))
