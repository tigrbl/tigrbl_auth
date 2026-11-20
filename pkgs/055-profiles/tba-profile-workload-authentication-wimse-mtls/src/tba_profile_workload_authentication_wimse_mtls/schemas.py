from dataclasses import dataclass

from tba_concrete_certificate_x509 import X509Certificate


@dataclass(frozen=True, slots=True)
class TLSPeer:
    """Peer evidence supplied by a trusted TLS endpoint."""

    certificate: X509Certificate
    intermediates: tuple[bytes, ...] = ()
    server_name: str | None = None
