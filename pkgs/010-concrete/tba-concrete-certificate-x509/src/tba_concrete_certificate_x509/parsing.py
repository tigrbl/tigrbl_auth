from cryptography import x509
from cryptography.hazmat.primitives.serialization import Encoding

from .certificate import X509Certificate


def parse_x509_certificate(data: bytes) -> X509Certificate:
    """Parse one DER or PEM certificate."""
    if data.lstrip().startswith(b"-----BEGIN CERTIFICATE-----"):
        certificates = x509.load_pem_x509_certificates(data)
        if len(certificates) != 1:
            raise ValueError("expected exactly one PEM certificate")
        data = certificates[0].public_bytes(Encoding.DER)
    return X509Certificate(data)
