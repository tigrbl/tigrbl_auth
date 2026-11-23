from typing import Protocol

from .certificates import (
    CertificatePathValidationRequest,
    CertificatePathValidationResult,
)


class CertificatePathValidatorPort(Protocol):
    def validate(
        self, request: CertificatePathValidationRequest, /
    ) -> CertificatePathValidationResult: ...


__all__ = ["CertificatePathValidatorPort"]
