from datetime import datetime, timezone
from hashlib import sha256

from tigrbl_security_trust_contracts import (
    CertificateStatus,
    CertificateStatusProviderPort,
    CertificateStatusResult,
)


class SnapshotCertificateStatusProvider(CertificateStatusProviderPort):
    def __init__(self):
        self._statuses: dict[bytes, CertificateStatusResult] = {}

    @staticmethod
    def _fingerprint(certificate_der: bytes) -> bytes:
        if not certificate_der:
            raise ValueError("certificate DER cannot be empty")
        return sha256(certificate_der).digest()

    def publish(
        self,
        certificate_der: bytes,
        status: CertificateStatus,
        source: str,
        checked_at: datetime | None = None,
    ) -> None:
        if not source:
            raise ValueError("certificate status source is required")
        self._statuses[self._fingerprint(certificate_der)] = CertificateStatusResult(
            status, checked_at or datetime.now(timezone.utc), source
        )

    def status(self, certificate_der: bytes, /) -> CertificateStatusResult:
        return self._statuses.get(
            self._fingerprint(certificate_der),
            CertificateStatusResult(
                CertificateStatus.UNKNOWN, datetime.now(timezone.utc), "none"
            ),
        )


__all__ = ["SnapshotCertificateStatusProvider"]
