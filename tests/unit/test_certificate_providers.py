from datetime import datetime, timezone

from tigrbl_certificate_path_validator import ProfiledCertificatePathValidator
from tigrbl_certificate_status_provider import SnapshotCertificateStatusProvider
from tigrbl_security_trust_contracts import (
    CertificateArtifact,
    CertificatePathValidationRequest,
    CertificatePathValidationResult,
    CertificateProfile,
    CertificateStatus,
    TrustAnchor,
)
from tigrbl_trust_anchor_provider import ProfiledTrustAnchorProvider


def _anchors():
    provider = ProfiledTrustAnchorProvider()
    provider.publish(
        TrustAnchor(
            "svid-root",
            b"root",
            (CertificateProfile.X509_SVID,),
        )
    )
    return provider


def _backend(request, anchors):
    return CertificatePathValidationResult(
        True,
        request.leaf.profile,
        anchors[0].identifier,
    )


def test_trust_anchors_are_profile_scoped():
    anchors = _anchors()
    assert len(anchors.anchors_for(CertificateProfile.X509_SVID)) == 1
    assert anchors.anchors_for(CertificateProfile.OAUTH_MTLS) == ()


def test_status_provider_defaults_unknown_and_tracks_revocation_snapshot():
    statuses = SnapshotCertificateStatusProvider()
    assert statuses.status(b"leaf").status is CertificateStatus.UNKNOWN
    statuses.publish(
        b"leaf",
        CertificateStatus.REVOKED,
        "ocsp",
        datetime.now(timezone.utc),
    )
    assert statuses.status(b"leaf").status is CertificateStatus.REVOKED


def test_path_validation_requires_explicit_profile_backend_anchor_and_status():
    statuses = SnapshotCertificateStatusProvider()
    request = CertificatePathValidationRequest(
        CertificateArtifact(b"leaf", CertificateProfile.X509_SVID)
    )
    validator = ProfiledCertificatePathValidator(
        _anchors(),
        statuses,
        {CertificateProfile.X509_SVID: _backend},
    )
    assert not validator.validate(request).valid
    statuses.publish(b"leaf", CertificateStatus.GOOD, "ocsp")
    assert validator.validate(request).valid


def test_validator_does_not_fallback_to_generic_pkix_or_ignore_revocation():
    statuses = SnapshotCertificateStatusProvider()
    statuses.publish(b"leaf", CertificateStatus.REVOKED, "crl")
    request = CertificatePathValidationRequest(
        CertificateArtifact(b"leaf", CertificateProfile.X509_SVID)
    )
    validator = ProfiledCertificatePathValidator(
        _anchors(),
        statuses,
        {CertificateProfile.X509_SVID: _backend},
    )
    assert validator.validate(request).errors == ("certificate is revoked",)
    unknown_profile = CertificatePathValidationRequest(
        CertificateArtifact(b"leaf", "custom")
    )
    assert validator.validate(unknown_profile).errors == (
        "unsupported certificate profile",
    )
