"""Construct the native CA from deployment credentials and enrollment policy."""

from tba_provider_certificate_issuer_x509 import X509CertificateIssuer, X509IssuerConfig
from tba_runtime_identity.workload.enrollment import ResolveWorkloadIdentity
from tba_runtime_identity.workload.wic_service import WicIssuanceService

from .settings import WicCaSettings


def build_wic_service(
    settings: WicCaSettings,
    *,
    resolve_identity: ResolveWorkloadIdentity,
    ca_key_password: bytes | None = None,
) -> WicIssuanceService:
    issuer = X509CertificateIssuer(
        X509IssuerConfig.from_pem(
            settings.ca_certificate_path.read_bytes(),
            settings.ca_private_key_path.read_bytes(),
            password=ca_key_password,
            max_lifetime_seconds=settings.lifetime_seconds,
        )
    )
    return WicIssuanceService(
        issuer,
        trust_domain=settings.trust_domain,
        resolve_identity=resolve_identity,
        lifetime_seconds=settings.lifetime_seconds,
    )
