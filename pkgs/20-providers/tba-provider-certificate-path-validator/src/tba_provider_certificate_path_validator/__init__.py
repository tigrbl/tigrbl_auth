from collections.abc import Callable, Sequence

from tba_contracts_security_trust import (
    CertificatePathValidationRequest,
    CertificatePathValidationResult,
    CertificateProfile,
    CertificateStatus,
    CertificateStatusProviderPort,
    TrustAnchor,
    TrustAnchorProviderPort,
)
from tba_bases_certificate import CertificatePathValidatorBase

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
        *,
        trust_domain: str | None = None,
    ):
        self._anchors = anchors
        self._trust_domain = trust_domain
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
        if self._trust_domain is None:
            anchors = self._anchors.anchors_for(profile)
        else:
            resolve = getattr(self._anchors, "anchors_for_domain", None)
            anchors = () if resolve is None else resolve(self._trust_domain, profile)
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
