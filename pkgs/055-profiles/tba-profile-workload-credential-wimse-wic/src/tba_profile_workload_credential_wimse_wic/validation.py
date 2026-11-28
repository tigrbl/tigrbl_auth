from tba_concrete_certificate_x509 import X509Certificate
from tba_concrete_wic import WorkloadIdentityCertificate
from tba_protocol_workload_wimse_identifier import WorkloadIdentifier


def validate_wic(certificate: X509Certificate) -> WorkloadIdentityCertificate:
    identifiers = [
        uri for uri in certificate.uri_sans if uri.lower().startswith("wimse:")
    ]
    if len(identifiers) != 1 or any(
        uri.lower().startswith("spiffe:") for uri in certificate.uri_sans
    ):
        raise ValueError("WIC requires exactly one native workload URI SAN")
    identifier = WorkloadIdentifier.parse(identifiers[0])
    return WorkloadIdentityCertificate(certificate, str(identifier))
