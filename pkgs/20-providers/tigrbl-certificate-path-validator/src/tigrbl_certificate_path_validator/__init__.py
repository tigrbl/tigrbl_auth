from collections.abc import Callable, Sequence

from tigrbl_security_trust_contracts import (
    CertificatePathValidationRequest,
    CertificatePathValidationResult,
    CertificateProfile,
    CertificateStatus,
    CertificateStatusProviderPort,
    TrustAnchor,
    TrustAnchorProviderPort,
)
from tigrbl_certificate_bases import CertificatePathValidatorBase

PathValidationBackend = Callable[
    [CertificatePathValidationRequest, Sequence[TrustAnchor]],
    CertificatePathValidationResult,
]


class ProfiledCertificatePathValidator(CertificatePathValidatorBase):
    def __init__(
        self,
        anchors: TrustAnchorProviderPort,
        status_provider: CertificateStatusProviderPort,
        backends: dict[CertificateProfile, PathValidationBackend],
        allow_unknown_status: set[CertificateProfile] | None = None,
    ):
        self._anchors = anchors
        self._status = status_provider
        self._backends = dict(backends)
        self._allow_unknown = set(allow_unknown_status or ())

    def validate(
        self, request: CertificatePathValidationRequest, /
    ) -> CertificatePathValidationResult:
        try:
            profile = CertificateProfile(request.leaf.profile)
        except ValueError:
            return CertificatePathValidationResult(
                False, request.leaf.profile, errors=("unsupported certificate profile",)
            )
        backend = self._backends.get(profile)
        if backend is None:
            return CertificatePathValidationResult(
                False, profile, errors=("no path-validation backend for profile",)
            )
        anchors = self._anchors.anchors_for(profile)
        if not anchors:
            return CertificatePathValidationResult(
                False, profile, errors=("no trust anchors for profile",)
            )
        result = backend(request, anchors)
        if result.profile != profile:
            return CertificatePathValidationResult(
                False,
                profile,
                errors=("backend returned the wrong validation profile",),
            )
        if not result.valid:
            return result
        status = self._status.status(request.leaf.der)
        if status.status is CertificateStatus.REVOKED:
            return CertificatePathValidationResult(
                False, profile, result.trust_anchor_id, ("certificate is revoked",)
            )
        if (
            status.status is CertificateStatus.UNKNOWN
            and profile not in self._allow_unknown
        ):
            return CertificatePathValidationResult(
                False,
                profile,
                result.trust_anchor_id,
                ("certificate status is unknown",),
            )
        return result


__all__ = ["PathValidationBackend", "ProfiledCertificatePathValidator"]
