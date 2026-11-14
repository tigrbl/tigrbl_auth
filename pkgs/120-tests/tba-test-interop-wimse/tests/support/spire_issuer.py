"""Isolated, server-minted SPIRE X.509-SVIDs for the WIC lab."""

from base64 import urlsafe_b64decode
from contextlib import contextmanager
from pathlib import Path
import json
import subprocess
from tempfile import TemporaryDirectory
from time import monotonic, sleep
from uuid import uuid4

from tba_testkit_workload_credential_conformance.fixtures import _certificate
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec

from tba_test_interop_wimse.wic import TlsFiles
from support.wic_fixture import write_leaf

IMAGE = "sha256:ff546f4c62dafc479a0cd79eae9a7b6df2975754d75efd31706098e0d7548837"
SPIRE = "/opt/spire/bin/spire-server"
CONFIG = """server {
    trust_domain = "example.org"
    bind_address = "127.0.0.1"
    bind_port = "8081"
    data_dir = "/tmp/wic-data"
    ca_subject { organization = ["WIC matrix lab"] }
    experimental { enable_wit_svids = true }
}
plugins {
    DataStore "sql" {
        plugin_data {
            database_type = "sqlite3"
            connection_string = "/tmp/wic-data/datastore.sqlite3"
        }
    }
    KeyManager "memory" { plugin_data {} }
    NodeAttestor "join_token" { plugin_data {} }
}
"""


def docker(*args, check=True):
    return subprocess.run(["docker", *map(str, args)], check=check, capture_output=True,
                          text=True, timeout=30)


class SpireIssuer:
    def __init__(self, container, directory):
        self.container = container
        self.directory = directory
        self.minted = {}
        self.wits = {}
        self.alternate = None
        self.bundle = directory / "spire-bundle.pem"
        self.bundle.write_text(docker("exec", container, SPIRE, "bundle", "show").stdout, encoding="ascii")

    def mint(self, identity):
        if identity in self.minted:
            return self.minted[identity]
        local = self.directory / uuid4().hex
        local.mkdir()
        output = "/tmp/wic-data"
        docker("exec", self.container, SPIRE, "x509", "mint", "-spiffeID", identity,
               "-ttl", "45m", "-write", output)
        docker("cp", f"{self.container}:{output}/svid.pem", local)
        docker("cp", f"{self.container}:{output}/key.pem", local)
        material = TlsFiles(str(local / "svid.pem"), str(local / "key.pem"), str(self.bundle))
        self.minted[identity] = material
        return material

    def mint_wit(self, identity, *, alternate=False):
        if alternate:
            return self.alternate.mint_wit(identity)
        if identity not in self.wits:
            local = self.directory / uuid4().hex
            local.mkdir()
            output = "/tmp/wic-data"
            docker("exec", self.container, SPIRE, "wit", "mint", "-spiffeID", identity,
                   "-write", output)
            for name in ("token", "key"):
                docker("cp", f"{self.container}:{output}/{name}", local)
            token = (local / "token").read_text(encoding="ascii").strip()
            private_jwk = json.loads((local / "key").read_bytes())
            if (private_jwk["kty"], private_jwk["crv"]) != ("EC", "P-256"):
                raise ValueError("unexpected SPIRE WIT-SVID proof key")
            scalar = int.from_bytes(urlsafe_b64decode(private_jwk["d"] + "="), "big")
            key = ec.derive_private_key(scalar, ec.SECP256R1())
            bundle = json.loads(docker("exec", self.container, SPIRE, "bundle", "show",
                                       "-format", "spiffe").stdout)
            from tba_concrete_jwt import decode_jwt_unverified

            kid = decode_jwt_unverified(token).jws.protected_headers["kid"]
            jwk, = (entry for entry in bundle["keys"]
                    if entry.get("use") == "wit-svid" and entry.get("kid") == kid)
            self.wits[identity] = token, key, {**jwk, "alg": "ES256"}
        return self.wits[identity]

    def issue_pair(self, directory, subjects, receiver):
        server = self.mint(receiver)
        if len(subjects) == 1 and subjects[0].startswith("spiffe://example.org/"):
            return self.mint(subjects[0]), server
        # SPIRE does not issue missing/multiple URI SANs. Inject a foreign leaf
        # only at the peer input, with a separate TLS test anchor for that leaf.
        foreign = _certificate(())
        tls_roots = directory / "tls-input-roots.pem"
        tls_roots.write_bytes(self.bundle.read_bytes() +
                              foreign[0].public_bytes(serialization.Encoding.PEM))
        client = write_leaf(directory, "malformed-input", _certificate(subjects, issuer=foreign),
                            self.bundle)
        return client, TlsFiles(server.certificate, server.private_key, str(tls_roots))


@contextmanager
def spire_issuer(parent, *, domain="example.org"):
    with TemporaryDirectory(dir=parent) as folder:
        directory = Path(folder)
        config = directory / "server.conf"
        config.write_text(CONFIG.replace('trust_domain = "example.org"', f'trust_domain = "{domain}"'), encoding="ascii")
        name = "tba-wic-matrix-" + uuid4().hex
        docker("create", "--name", name, "--network", "none", IMAGE, "-config", "/server.conf")
        try:
            docker("cp", config, f"{name}:/server.conf")
            docker("start", name)
            deadline = monotonic() + 15
            while docker("exec", name, SPIRE, "healthcheck", check=False).returncode:
                if monotonic() >= deadline:
                    raise ValueError(docker("logs", name).stderr)
                sleep(.2)
            issuer = SpireIssuer(name, directory)
            yield issuer
        finally:
            docker("rm", "-f", name)


@contextmanager
def spire_wit_issuers(parent):
    with (spire_issuer(parent) as issuer, spire_issuer(parent) as wrong_anchor,
          spire_issuer(parent, domain="other.example") as foreign):
        issuer.alternate = wrong_anchor
        issuer.foreign = foreign
        yield issuer
