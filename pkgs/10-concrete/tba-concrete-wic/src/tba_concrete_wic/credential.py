from dataclasses import dataclass

from tba_concrete_certificate_x509 import X509Certificate


@dataclass(frozen=True, slots=True)
class WorkloadIdentityCertificate:
    certificate: X509Certificate
    workload_identifier: str
