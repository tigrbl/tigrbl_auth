"""Explicit SPIFFE X.509-SVID composition for fixture TLS peers."""
from datetime import datetime, timezone

from tba_concrete_certificate_x509 import parse_x509_certificate
from tba_contracts_security_trust import CertificateArtifact, CertificatePathValidationRequest, CertificateStatus
from tba_protocol_workload_spiffe_svid.x509_svid import validate_x509_svid

from .wic import WorkloadVerifier


class SpiffeWicVerifier(WorkloadVerifier):
    workload_name_only = True

    def verify(self, certificate, *, dns_name=None):
        leaf = parse_x509_certificate(certificate)
        if leaf.key_usage is None or leaf.basic_constraints is None:
            raise ValueError("SPIFFE peer needs key usage and basic constraints")
        identity = validate_x509_svid(
            uri_sans=leaf.uri_sans, dns_sans=leaf.dns_sans,
            key_usage_digital_signature=leaf.key_usage.digital_signature,
            basic_constraints_ca=leaf.basic_constraints.ca,
        )
        if identity != self.expected_identity:
            raise ValueError("unexpected WIMSE peer identity")
        domain = identity.removeprefix("spiffe://").partition("/")[0]
        validator = self.validators.get(domain)
        if validator is None:
            raise ValueError("no configured SPIFFE path validator")
        now = datetime.now(timezone.utc)
        result = validator.validate(CertificatePathValidationRequest(
            CertificateArtifact(leaf.der, "spiffe-x509-svid"), (), now,
        ))
        if not result.valid or result.indeterminate or not leaf.not_before <= now <= leaf.not_after:
            raise ValueError("SPIFFE peer path or validity was not verified")
        if self.status.status(leaf.der).status != CertificateStatus.GOOD:
            raise ValueError("SPIFFE peer certificate status was not confirmed")
        return identity
