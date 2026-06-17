from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for src in sorted((ROOT / "pkgs").glob("*/src")):
    value = str(src)
    if value not in sys.path:
        sys.path.insert(0, value)


def test_dpop_key_credential_t0_public_model_is_importable() -> None:
    import tigrbl_authn_credentials as credentials

    dpop = credentials.create_dpop_key_credential(
        "service:billing",
        jwk_thumbprint="thumb-dpop",
        public_jwk={"kty": "EC", "crv": "P-256", "kid": "kid-1"},
    )

    assert isinstance(dpop, credentials.DpopKeyCredential)
    assert dpop.confirmation_claim == {"jkt": "thumb-dpop"}
    assert dpop.to_credential().kind is credentials.CredentialKind.DPOP_KEY


def test_dpop_key_credential_t1_renders_confirmation_claim_and_lifecycle_credential() -> None:
    import tigrbl_authn_credentials as credentials

    dpop = credentials.create_dpop_key_credential(
        "service:billing",
        jwk_thumbprint="thumb-dpop",
        public_jwk={"kty": "EC", "crv": "P-256", "kid": "kid-1"},
        metadata={"issuer": "https://issuer.example.test"},
    )
    binding = credentials.ProofBinding.for_dpop(dpop)
    credential = dpop.to_credential()

    assert binding.method == "dpop"
    assert binding.credential_id == dpop.id
    assert binding.confirmation_claim == {"jkt": "thumb-dpop"}
    assert credential.public_id == "thumb-dpop"
    assert credential.metadata["public_jwk"]["kid"] == "kid-1"


def test_dpop_key_credential_t2_rejects_blank_or_malformed_proof_material() -> None:
    import pytest
    import tigrbl_authn_credentials as credentials

    with pytest.raises(ValueError, match="JWK thumbprint is required"):
        credentials.create_dpop_key_credential(
            "service:billing",
            jwk_thumbprint="  ",
        )

    with pytest.raises(ValueError, match="principal id is required"):
        credentials.create_dpop_key_credential(
            "  ",
            jwk_thumbprint="thumb-dpop",
        )

    with pytest.raises(ValueError, match="public_jwk must be a mapping"):
        credentials.DpopKeyCredential(
            "service:billing",
            jwk_thumbprint="thumb-dpop",
            public_jwk=["not-a-mapping"],  # type: ignore[arg-type]
        )
