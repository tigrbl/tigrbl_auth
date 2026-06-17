from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for src in sorted((ROOT / "pkgs").glob("*/src")):
    value = str(src)
    if value not in sys.path:
        sys.path.insert(0, value)


def test_mtls_certificate_credential_t0_public_model_is_importable() -> None:
    import tigrbl_authn_credentials as credentials

    mtls = credentials.create_mtls_certificate_credential(
        "service:billing",
        certificate_thumbprint="thumb-mtls",
        subject_dn="CN=client.example",
        san_dns=("client.example",),
    )

    assert isinstance(mtls, credentials.MtlsCertificateCredential)
    assert mtls.confirmation_claim == {"x5t#S256": "thumb-mtls"}
    assert mtls.to_credential().kind is credentials.CredentialKind.MTLS_CERTIFICATE


def test_proof_binding_t1_renders_dpop_and_mtls_confirmation_claims() -> None:
    import tigrbl_authn_credentials as credentials

    mtls = credentials.create_mtls_certificate_credential(
        "service:billing",
        certificate_thumbprint="thumb-mtls",
    )
    mtls_binding = credentials.ProofBinding.for_mtls(mtls)
    dpop_binding = credentials.ProofBinding.for_dpop("thumb-jkt", credential_id="cred-dpop")

    assert mtls_binding.method == "mtls"
    assert mtls_binding.confirmation_claim == {"x5t#S256": "thumb-mtls"}
    assert dpop_binding.method == "dpop"
    assert dpop_binding.confirmation_claim == {"jkt": "thumb-jkt"}
