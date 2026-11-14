"""Network fixtures for WIC/mTLS interoperability on a test host."""

from dataclasses import dataclass
from pathlib import Path
import ssl

from cryptography import x509
from cryptography.exceptions import InvalidSignature
from tba_concrete_certificate_x509 import parse_x509_certificate
from tba_contracts_security_trust import CertificatePathValidationResult, CertificateStatus
from tba_profile_workload_authentication_wimse_mtls import TLSPeer, verify_wimse_peer
from tba_provider_certificate_status import SnapshotCertificateStatusProvider

from .http_fixture import FixtureConnection, FixtureServer, call_resource


@dataclass(frozen=True)
class TlsFiles:
    certificate: str
    private_key: str
    trust_anchor: str

    def context(self, *, server):
        purpose = ssl.Purpose.CLIENT_AUTH if server else ssl.Purpose.SERVER_AUTH
        context = ssl.create_default_context(purpose, cafile=self.trust_anchor)
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_cert_chain(self.certificate, self.private_key)
        return context


class DirectCertificatePath:
    """A single test CA signs each leaf. TLS also validates peer certificates."""

    def __init__(self, anchor):
        self.anchor = x509.load_pem_x509_certificate(Path(anchor).read_bytes())

    def validate(self, request):
        leaf = x509.load_der_x509_certificate(request.leaf.der)
        try:
            leaf.verify_directly_issued_by(self.anchor)
        except (ValueError, TypeError, InvalidSignature):
            return CertificatePathValidationResult(False, request.leaf.profile)
        return CertificatePathValidationResult(True, request.leaf.profile)


def certificate_status(good_certificates):
    provider = SnapshotCertificateStatusProvider()
    for filename in good_certificates:
        der = parse_x509_certificate(Path(filename).read_bytes()).der
        provider.publish(der, CertificateStatus.GOOD, "explicit-fixture-status")
    return provider


class WorkloadVerifier:
    def __init__(self, expected_identity, domain_anchors, status_provider):
        self.expected_identity = expected_identity
        self.validators = {
            domain: DirectCertificatePath(path) for domain, path in domain_anchors.items()
        }
        self.status = status_provider

    def verify(self, certificate, *, dns_name=None):
        return verify_wimse_peer(
            TLSPeer(parse_x509_certificate(certificate), server_name=dns_name),
            expected_identity=self.expected_identity,
            validators_by_domain=self.validators,
            status_provider=self.status,
        ).workload_identifier


class WicReceiver(FixtureServer):
    """Loopback fixture exposing POST /writes and GET /effects."""

    denial_status = 403

    def __init__(self, port, tls, verifier, ledger=None):
        self.verifier = verifier
        super().__init__(port, tls.context(server=True), ledger)

    def authenticate(self, request, path):
        return self.verifier.verify(request.connection.getpeercert(binary_form=True))


class _VerifiedConnection(FixtureConnection):
    def __init__(self, host, port, dns_name, tls, verifier):
        super().__init__(host, port, dns_name, tls.context(server=False))
        self.verifier = verifier

    def connect(self):
        super().connect()
        try:
            self.verifier.verify(self.sock.getpeercert(binary_form=True), dns_name=self.dns_name)
        except ValueError as error:
            self.close()
            raise RejectedServerIdentity(str(error)) from error
        except BaseException:
            self.close()
            raise


class RejectedServerIdentity(ValueError):
    """TLS succeeded but the configured workload identity policy denied the peer."""


@dataclass(frozen=True)
class WicCaller:
    tls: TlsFiles
    verifier: WorkloadVerifier

    def request(self, host, port, dns_name, *, readback=False):
        connection = _VerifiedConnection(host, port, dns_name, self.tls, self.verifier)
        return call_resource(connection, readback=readback)
