from datetime import datetime, timezone

from tba_contracts_security_trust import (
    CertificateArtifact,
    CertificatePathValidationRequest,
    CertificateStatus,
)
from tba_profile_workload_credential_wimse_wic import validate_wic
from tba_protocol_workload_wimse_identifier import WorkloadIdentifier

from .schemas import TLSPeer


def verify_wimse_peer(
    peer: TLSPeer,
    *,
    expected_identity: str,
    validators_by_domain,
    status_provider,
    now=None,
):
    """Apply workload policy to a certificate obtained from an authenticated TLS peer."""
    expected = WorkloadIdentifier.parse(expected_identity)
    credential = validate_wic(peer.certificate)
    if credential.workload_identifier != str(expected):
        raise ValueError("unexpected WIMSE peer identity")
    validator = validators_by_domain.get(expected.trust_domain)
    if validator is None:
        raise ValueError("WIMSE trust domain has no configured path validator")
    now = datetime.now(timezone.utc) if now is None else now
    if not peer.certificate.not_before <= now <= peer.certificate.not_after:
        raise ValueError("WIMSE peer certificate is outside its validity period")
    if peer.server_name is not None:
        hostname = peer.server_name.lower()
        dns_names = {name.lower() for name in peer.certificate.dns_sans}
        wildcard = "*." + hostname.partition(".")[2]
        if hostname not in dns_names and (
            "." not in hostname or wildcard not in dns_names
        ):
            raise ValueError(
                "WIMSE peer certificate does not match the TLS server name"
            )
    result = validator.validate(
        CertificatePathValidationRequest(
            CertificateArtifact(peer.certificate.der, "wimse-wic"),
            peer.intermediates,
            now,
        )
    )
    if not result.valid or result.indeterminate or result.profile != "wimse-wic":
        raise ValueError("WIMSE peer certificate path was not verified")
    if status_provider.status(peer.certificate.der).status != CertificateStatus.GOOD:
        raise ValueError("WIMSE peer certificate status was not confirmed")
    return credential
