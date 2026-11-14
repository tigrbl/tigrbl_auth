"""Explicit WIC and application-proof caller composition."""
from dataclasses import dataclass

from .http_fixture import call_resource
from .wic import TlsFiles, WorkloadVerifier, _VerifiedConnection
from .wpt import WptCaller


@dataclass(frozen=True)
class CombinedCaller:
    application: WptCaller
    tls: TlsFiles
    verifier: WorkloadVerifier

    def request(self, host, port, dns_name, *, readback=False, headers=None):
        if headers is None:
            headers = self.application.present(dns_name, port, readback=readback)
        return call_resource(
            self.connection(host, port, dns_name),
            readback=readback, headers=headers,
        )

    def connection(self, host, port, dns_name):
        return _VerifiedConnection(host, port, dns_name, self.tls, self.verifier)
