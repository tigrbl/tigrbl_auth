"""Pinned SPIRE Agent Workload API fixture for acquired X.509-SVIDs."""

from contextlib import contextmanager
import json
from pathlib import Path
from time import monotonic, sleep
from uuid import uuid4

from cryptography import x509
from tba_test_interop_wimse.wic import TlsFiles

from support.spire_issuer import SPIRE, docker


AGENT_IMAGE = "sha256:ab3a8ce70435374cc5d84c81eabf0278dc046ddbc0a736d59694ba9e5975b1b6"
AGENT = "/opt/spire/bin/spire-agent"
SOCKET = "/tmp/tba-workload.sock"
OUTPUT = "/tmp/tba-acquired"
CONFIG = """
agent {
    trust_domain = "example.org"
    trust_bundle_path = "/tmp/bootstrap.pem"
    server_address = "127.0.0.1"
    server_port = 8081
    data_dir = "/tmp/agent-state"
    socket_path = "/tmp/tba-workload.sock"
}
plugins {
    KeyManager "memory" { plugin_data {} }
    NodeAttestor "join_token" { plugin_data {} }
    WorkloadAttestor "unix" { plugin_data {} }
}
"""


class SpireWorkloadApi:
    def __init__(self, container, directory, issuer):
        self.container, self.directory, self.issuer = container, directory, issuer

    def command(self, *, uid=0, output=False):
        options = ["-u", str(uid), self.container, AGENT, "api", "fetch", "x509",
                   "-socketPath", SOCKET, "-timeout", "2s"]
        if output:
            options.extend(("-write", OUTPUT))
        return docker("exec", *options, check=False)

    def fetch(self, *, enrolled):
        if not enrolled:
            reply = self.command(uid=1001)
            detail = (reply.stderr + reply.stdout).lower()
            if reply.returncode and ("no identity issued" in detail or "permissiondenied" in detail
                                     or "not entitled" in detail):
                return None
            raise ValueError(f"SPIRE Agent returned an unexpected unregistered-workload result: {detail}")
        reply = self.command(output=True)
        if reply.returncode:
            raise ValueError(reply.stderr)
        return self.read_fetched()

    def read_fetched(self):
        # The CLI writes all context artifacts. Materialize the response as a
        # separate local directory and preserve the returned trust bundle.
        directory = self.directory / uuid4().hex
        directory.mkdir()
        docker("cp", f"{self.container}:{OUTPUT}/.", directory)
        credential = directory / "svid.0.pem"
        key = directory / "svid.0.key"
        bundle = directory / "bundle.0.pem"
        certificate = x509.load_pem_x509_certificates(credential.read_bytes())[0]
        identity, = certificate.extensions.get_extension_for_class(x509.SubjectAlternativeName).value
        if identity.value != "spiffe://example.org/workload-0" or not key.is_file() or not bundle.is_file():
            raise ValueError("Unexpected Workload API identity or trust bundle")
        return TlsFiles(str(credential), str(key), str(bundle))

    def with_acquired(self, material):
        return AcquiredIssuer(self.issuer, material)


class AcquiredIssuer:
    def __init__(self, issuer, material):
        self.issuer = issuer
        self.material = material
        self.used = False

    def __getattr__(self, name):
        return getattr(self.issuer, name)

    def issue_pair(self, directory, subjects, receiver):
        if subjects == ("spiffe://example.org/workload-0",) and receiver == "spiffe://example.org/workload-1":
            self.used = True
            return self.material, self.issuer.mint(receiver)
        return self.issuer.issue_pair(directory, subjects, receiver)


@contextmanager
def spire_workload_api(issuer, directory):
    config = Path(directory) / "agent.conf"
    config.write_text(CONFIG, encoding="ascii")
    output = docker("exec", issuer.container, SPIRE, "token", "generate", "-output", "json").stdout
    token = json.loads(output)["value"]
    token_file = Path(directory) / "join-token"
    token_file.write_text(token, encoding="ascii")
    response = Path(directory) / "response"
    response.mkdir()
    name = "tba-workload-api-" + uuid4().hex
    docker("create", "--name", name, "--network", f"container:{issuer.container}", AGENT_IMAGE,
           "-config", "/tmp/agent.conf", "-joinTokenFile", "/tmp/join-token")
    try:
        docker("cp", config, f"{name}:/tmp/agent.conf")
        docker("cp", token_file, f"{name}:/tmp/join-token")
        docker("cp", issuer.bundle, f"{name}:/tmp/bootstrap.pem")
        docker("cp", response, f"{name}:{OUTPUT}")
        docker("exec", issuer.container, SPIRE, "entry", "create",
               "-parentID", f"spiffe://example.org/spire/agent/join_token/{token}",
               "-spiffeID", "spiffe://example.org/workload-0", "-selector", "unix:uid:0")
        docker("start", name)
        deadline = monotonic() + 25
        agent = SpireWorkloadApi(name, directory, issuer)
        while agent.command().returncode:
            if monotonic() >= deadline:
                raise ValueError("SPIRE Agent did not serve its registered Workload API identity")
            sleep(.25)
        yield agent
    finally:
        docker("rm", "-f", name)
