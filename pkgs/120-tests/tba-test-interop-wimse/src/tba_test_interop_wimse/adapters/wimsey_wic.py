"""Use the pinned wimsey WIC verifier in a shared TLS endpoint fixture."""

import json
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

WIMSEY_REVISION = "56b070582f3e380c5006630698fb4ca808c08b04"


class WimseyVerifier:
    """The CLI verifies certificate and URI; the wrapper checks the expected URI."""

    def __init__(self, binary, anchor, expected_identity, *, status_provider=None):
        self.binary = Path(binary).resolve()
        self.anchor = Path(anchor).resolve()
        self.expected_identity = expected_identity
        self.workload_name_only = expected_identity.startswith("spiffe://")
        self.status_provider = status_provider

    def verify(self, certificate, *, dns_name=None):
        with TemporaryDirectory() as directory:
            leaf = Path(directory) / "peer.der"
            leaf.write_bytes(certificate)
            result = subprocess.run(
                [str(self.binary), "wic", "verify", "--cert", str(leaf), "--ca", str(self.anchor)],
                capture_output=True, text=True, timeout=10,
            )
        if result.returncode:
            message = result.stderr.strip()
            if not message.startswith("error:"):
                raise RuntimeError(f"wimsey verifier failed to execute: {message}")
            raise ValueError(message)
        identity = json.loads(result.stdout)["sub"]
        if identity != self.expected_identity:
            raise ValueError("unexpected wimsey peer identity")
        if self.status_provider is not None:
            from tba_contracts_security_trust import CertificateStatus

            if self.status_provider.status(certificate).status != CertificateStatus.GOOD:
                raise ValueError("wimsey fixture peer certificate status was not confirmed")
        return identity
